"""Support KNX devices."""
from __future__ import annotations

import asyncio
import logging
from typing import Final

import voluptuous as vol
from xknx import XKNX
from xknx.core import XknxConnectionState
from xknx.core.telegram_queue import TelegramQueue
from xknx.dpt import DPTArray, DPTBase, DPTBinary
from xknx.exceptions import XKNXException
from xknx.io import ConnectionConfig, ConnectionType
from xknx.telegram import AddressFilter, Telegram
from xknx.telegram.address import parse_device_group_address
from xknx.telegram.apci import GroupValueRead, GroupValueResponse, GroupValueWrite

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    EVENT_HOMEASSISTANT_STOP,
    SERVICE_RELOAD,
)
from homeassistant.core import Event, HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.reload import async_integration_yaml_config
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_KNX_EXPOSE,
    CONF_KNX_INDIVIDUAL_ADDRESS,
    CONF_KNX_ROUTING,
    CONF_KNX_TUNNELING,
    DOMAIN,
    KNX_ADDRESS,
    SupportedPlatforms,
)
from .expose import KNXExposeSensor, KNXExposeTime, create_knx_exposure
from .schema import (
    BinarySensorSchema,
    ClimateSchema,
    ConnectionSchema,
    CoverSchema,
    ExposeSchema,
    FanSchema,
    LightSchema,
    NotifySchema,
    NumberSchema,
    SceneSchema,
    SelectSchema,
    SensorSchema,
    SwitchSchema,
    WeatherSchema,
    ga_validator,
    sensor_type_validator,
)

_LOGGER = logging.getLogger(__name__)


CONF_KNX_FIRE_EVENT: Final = "fire_event"
CONF_KNX_EVENT_FILTER: Final = "event_filter"

SERVICE_KNX_SEND: Final = "send"
SERVICE_KNX_ATTR_PAYLOAD: Final = "payload"
SERVICE_KNX_ATTR_TYPE: Final = "type"
SERVICE_KNX_ATTR_REMOVE: Final = "remove"
SERVICE_KNX_EVENT_REGISTER: Final = "event_register"
SERVICE_KNX_EXPOSURE_REGISTER: Final = "exposure_register"
SERVICE_KNX_READ: Final = "read"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            # deprecated since 2021.4
            cv.deprecated("config_file"),
            # deprecated since 2021.2
            cv.deprecated(CONF_KNX_FIRE_EVENT),
            cv.deprecated("fire_event_filter", replacement_key=CONF_KNX_EVENT_FILTER),
            vol.Schema(
                {
                    **ConnectionSchema.SCHEMA,
                    vol.Optional(CONF_KNX_FIRE_EVENT): cv.boolean,
                    vol.Optional(CONF_KNX_EVENT_FILTER, default=[]): vol.All(
                        cv.ensure_list, [cv.string]
                    ),
                    **ExposeSchema.platform_node(),
                    **BinarySensorSchema.platform_node(),
                    **ClimateSchema.platform_node(),
                    **CoverSchema.platform_node(),
                    **FanSchema.platform_node(),
                    **LightSchema.platform_node(),
                    **NotifySchema.platform_node(),
                    **NumberSchema.platform_node(),
                    **SceneSchema.platform_node(),
                    **SelectSchema.platform_node(),
                    **SensorSchema.platform_node(),
                    **SwitchSchema.platform_node(),
                    **WeatherSchema.platform_node(),
                }
            ),
        )
    },
    extra=vol.ALLOW_EXTRA,
)

SERVICE_KNX_SEND_SCHEMA = vol.Any(
    vol.Schema(
        {
            vol.Required(KNX_ADDRESS): vol.All(
                cv.ensure_list,
                [ga_validator],
            ),
            vol.Required(SERVICE_KNX_ATTR_PAYLOAD): cv.match_all,
            vol.Required(SERVICE_KNX_ATTR_TYPE): sensor_type_validator,
        }
    ),
    vol.Schema(
        # without type given payload is treated as raw bytes
        {
            vol.Required(KNX_ADDRESS): vol.All(
                cv.ensure_list,
                [ga_validator],
            ),
            vol.Required(SERVICE_KNX_ATTR_PAYLOAD): vol.Any(
                cv.positive_int, [cv.positive_int]
            ),
        }
    ),
)

SERVICE_KNX_READ_SCHEMA = vol.Schema(
    {
        vol.Required(KNX_ADDRESS): vol.All(
            cv.ensure_list,
            [ga_validator],
        )
    }
)

SERVICE_KNX_EVENT_REGISTER_SCHEMA = vol.Schema(
    {
        vol.Required(KNX_ADDRESS): vol.All(
            cv.ensure_list,
            [ga_validator],
        ),
        vol.Optional(SERVICE_KNX_ATTR_REMOVE, default=False): cv.boolean,
    }
)

SERVICE_KNX_EXPOSURE_REGISTER_SCHEMA = vol.Any(
    ExposeSchema.EXPOSE_SENSOR_SCHEMA.extend(
        {
            vol.Optional(SERVICE_KNX_ATTR_REMOVE, default=False): cv.boolean,
        }
    ),
    vol.Schema(
        # for removing only `address` is required
        {
            vol.Required(KNX_ADDRESS): ga_validator,
            vol.Required(SERVICE_KNX_ATTR_REMOVE): vol.All(cv.boolean, True),
        },
        extra=vol.ALLOW_EXTRA,
    ),
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the KNX integration."""
    try:
        knx_module = KNXModule(hass, config)
        hass.data[DOMAIN] = knx_module
        await knx_module.start()
    except XKNXException as ex:
        _LOGGER.warning("Could not connect to KNX interface: %s", ex)
        hass.components.persistent_notification.async_create(
            f"Could not connect to KNX interface: <br><b>{ex}</b>", title="KNX"
        )

    if CONF_KNX_EXPOSE in config[DOMAIN]:
        for expose_config in config[DOMAIN][CONF_KNX_EXPOSE]:
            knx_module.exposures.append(
                create_knx_exposure(hass, knx_module.xknx, expose_config)
            )

    for platform in SupportedPlatforms:
        if platform.value not in config[DOMAIN]:
            continue
        hass.async_create_task(
            discovery.async_load_platform(
                hass,
                platform.value,
                DOMAIN,
                {
                    "platform_config": config[DOMAIN][platform.value],
                },
                config,
            )
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_KNX_SEND,
        knx_module.service_send_to_knx_bus,
        schema=SERVICE_KNX_SEND_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_KNX_READ,
        knx_module.service_read_to_knx_bus,
        schema=SERVICE_KNX_READ_SCHEMA,
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_KNX_EVENT_REGISTER,
        knx_module.service_event_register_modify,
        schema=SERVICE_KNX_EVENT_REGISTER_SCHEMA,
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_KNX_EXPOSURE_REGISTER,
        knx_module.service_exposure_register_modify,
        schema=SERVICE_KNX_EXPOSURE_REGISTER_SCHEMA,
    )

    async def reload_service_handler(service_call: ServiceCall) -> None:
        """Remove all KNX components and load new ones from config."""

        # First check for config file. If for some reason it is no longer there
        # or knx is no longer mentioned, stop the reload.
        config = await async_integration_yaml_config(hass, DOMAIN)

        if not config or DOMAIN not in config:
            return

        await knx_module.xknx.stop()

        await asyncio.gather(
            *(platform.async_reset() for platform in async_get_platforms(hass, DOMAIN))
        )

        await async_setup(hass, config)

    async_register_admin_service(
        hass, DOMAIN, SERVICE_RELOAD, reload_service_handler, schema=vol.Schema({})
    )

    return True


class KNXModule:
    """Representation of KNX Object."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        """Initialize KNX module."""
        self.hass = hass
        self.config = config
        self.connected = False
        self.exposures: list[KNXExposeSensor | KNXExposeTime] = []
        self.service_exposures: dict[str, KNXExposeSensor | KNXExposeTime] = {}

        self.init_xknx()
        self._knx_event_callback: TelegramQueue.Callback = self.register_callback()
        self.xknx.connection_manager.register_connection_state_changed_cb(
            self.connection_state_changed_cb
        )

    def init_xknx(self) -> None:
        """Initialize XKNX object."""
        self.xknx = XKNX(
            own_address=self.config[DOMAIN][CONF_KNX_INDIVIDUAL_ADDRESS],
            rate_limit=self.config[DOMAIN][ConnectionSchema.CONF_KNX_RATE_LIMIT],
            multicast_group=self.config[DOMAIN][ConnectionSchema.CONF_KNX_MCAST_GRP],
            multicast_port=self.config[DOMAIN][ConnectionSchema.CONF_KNX_MCAST_PORT],
            connection_config=self.connection_config(),
            state_updater=self.config[DOMAIN][ConnectionSchema.CONF_KNX_STATE_UPDATER],
        )

    async def start(self) -> None:
        """Start XKNX object. Connect to tunneling or Routing device."""
        await self.xknx.start()
        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)
        self.connected = True

    async def stop(self, event: Event) -> None:
        """Stop XKNX object. Disconnect from tunneling or Routing device."""
        await self.xknx.stop()

    def connection_config(self) -> ConnectionConfig:
        """Return the connection_config."""
        if CONF_KNX_TUNNELING in self.config[DOMAIN]:
            return self.connection_config_tunneling()
        if CONF_KNX_ROUTING in self.config[DOMAIN]:
            return self.connection_config_routing()
        return ConnectionConfig(auto_reconnect=True)

    def connection_config_routing(self) -> ConnectionConfig:
        """Return the connection_config if routing is configured."""
        local_ip = None
        # all configuration values are optional
        if self.config[DOMAIN][CONF_KNX_ROUTING] is not None:
            local_ip = self.config[DOMAIN][CONF_KNX_ROUTING].get(
                ConnectionSchema.CONF_KNX_LOCAL_IP
            )
        return ConnectionConfig(
            connection_type=ConnectionType.ROUTING, local_ip=local_ip
        )

    def connection_config_tunneling(self) -> ConnectionConfig:
        """Return the connection_config if tunneling is configured."""
        gateway_ip = self.config[DOMAIN][CONF_KNX_TUNNELING][CONF_HOST]
        gateway_port = self.config[DOMAIN][CONF_KNX_TUNNELING][CONF_PORT]
        local_ip = self.config[DOMAIN][CONF_KNX_TUNNELING].get(
            ConnectionSchema.CONF_KNX_LOCAL_IP
        )
        route_back = self.config[DOMAIN][CONF_KNX_TUNNELING][
            ConnectionSchema.CONF_KNX_ROUTE_BACK
        ]
        return ConnectionConfig(
            connection_type=ConnectionType.TUNNELING,
            gateway_ip=gateway_ip,
            gateway_port=gateway_port,
            local_ip=local_ip,
            route_back=route_back,
            auto_reconnect=True,
        )

    async def telegram_received_cb(self, telegram: Telegram) -> None:
        """Call invoked after a KNX telegram was received."""
        data = None
        # Not all telegrams have serializable data.
        if (
            isinstance(telegram.payload, (GroupValueWrite, GroupValueResponse))
            and telegram.payload.value is not None
        ):
            data = telegram.payload.value.value

        self.hass.bus.async_fire(
            "knx_event",
            {
                "data": data,
                "destination": str(telegram.destination_address),
                "direction": telegram.direction.value,
                "source": str(telegram.source_address),
                "telegramtype": telegram.payload.__class__.__name__,
            },
        )

    async def connection_state_changed_cb(self, state: XknxConnectionState) -> None:
        """Call invoked after a KNX connection state change was received."""
        self.connected = state == XknxConnectionState.CONNECTED
        if tasks := [device.after_update() for device in self.xknx.devices]:
            await asyncio.gather(*tasks)

    def register_callback(self) -> TelegramQueue.Callback:
        """Register callback within XKNX TelegramQueue."""
        address_filters = list(
            map(AddressFilter, self.config[DOMAIN][CONF_KNX_EVENT_FILTER])
        )
        return self.xknx.telegram_queue.register_telegram_received_cb(
            self.telegram_received_cb,
            address_filters=address_filters,
            group_addresses=[],
            match_for_outgoing=True,
        )

    async def service_event_register_modify(self, call: ServiceCall) -> None:
        """Service for adding or removing a GroupAddress to the knx_event filter."""
        attr_address = call.data[KNX_ADDRESS]
        group_addresses = map(parse_device_group_address, attr_address)

        if call.data.get(SERVICE_KNX_ATTR_REMOVE):
            for group_address in group_addresses:
                try:
                    self._knx_event_callback.group_addresses.remove(group_address)
                except ValueError:
                    _LOGGER.warning(
                        "Service event_register could not remove event for '%s'",
                        str(group_address),
                    )
            return

        for group_address in group_addresses:
            if group_address in self._knx_event_callback.group_addresses:
                continue
            self._knx_event_callback.group_addresses.append(group_address)
            _LOGGER.debug(
                "Service event_register registered event for '%s'",
                str(group_address),
            )

    async def service_exposure_register_modify(self, call: ServiceCall) -> None:
        """Service for adding or removing an exposure to KNX bus."""
        group_address = call.data[KNX_ADDRESS]

        if call.data.get(SERVICE_KNX_ATTR_REMOVE):
            try:
                removed_exposure = self.service_exposures.pop(group_address)
            except KeyError as err:
                raise HomeAssistantError(
                    f"Could not find exposure for '{group_address}' to remove."
                ) from err
            else:
                removed_exposure.shutdown()
            return

        if group_address in self.service_exposures:
            replaced_exposure = self.service_exposures.pop(group_address)
            _LOGGER.warning(
                "Service exposure_register replacing already registered exposure for '%s' - %s",
                group_address,
                replaced_exposure.device.name,
            )
            replaced_exposure.shutdown()
        exposure = create_knx_exposure(self.hass, self.xknx, call.data)  # type: ignore[arg-type]
        self.service_exposures[group_address] = exposure
        _LOGGER.debug(
            "Service exposure_register registered exposure for '%s' - %s",
            group_address,
            exposure.device.name,
        )

    async def service_send_to_knx_bus(self, call: ServiceCall) -> None:
        """Service for sending an arbitrary KNX message to the KNX bus."""
        attr_address = call.data[KNX_ADDRESS]
        attr_payload = call.data[SERVICE_KNX_ATTR_PAYLOAD]
        attr_type = call.data.get(SERVICE_KNX_ATTR_TYPE)

        payload: DPTBinary | DPTArray
        if attr_type is not None:
            transcoder = DPTBase.parse_transcoder(attr_type)
            if transcoder is None:
                raise ValueError(f"Invalid type for knx.send service: {attr_type}")
            payload = DPTArray(transcoder.to_knx(attr_payload))
        elif isinstance(attr_payload, int):
            payload = DPTBinary(attr_payload)
        else:
            payload = DPTArray(attr_payload)

        for address in attr_address:
            telegram = Telegram(
                destination_address=parse_device_group_address(address),
                payload=GroupValueWrite(payload),
            )
            await self.xknx.telegrams.put(telegram)

    async def service_read_to_knx_bus(self, call: ServiceCall) -> None:
        """Service for sending a GroupValueRead telegram to the KNX bus."""
        for address in call.data[KNX_ADDRESS]:
            telegram = Telegram(
                destination_address=parse_device_group_address(address),
                payload=GroupValueRead(),
            )
            await self.xknx.telegrams.put(telegram)
