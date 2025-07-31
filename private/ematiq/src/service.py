import asyncio
import json
import logging

import dotenv
import pendulum
import websockets

from external import ExchangeRateError, fetch_exchange_rate

type JSON = int | str | float | bool | None | dict[str, JSON] | list[JSON]
type JSONObject = dict[str, JSON]

WSS_URI = "wss://currency-assignment.ematiq.com"

HEARTBEAT_INTERVAL_SECONDS = 1
HEARTBEAT_THRESHOLD_SECONDS = 2

log = logging.getLogger()


async def send_heartbeat_periodically(connection: websockets.ClientConnection) -> None:
    """
    Send heartbeat messages to the web socket connection periodically.
    """
    while True:
        await connection.send(json.dumps({"type": "heartbeat"}))
        log.info("Heartbeat sent")
        await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)


async def process_conversion_request(
    connection: websockets.ClientConnection,
    data: JSONObject,
) -> None:
    """
    Process a currency conversion request and send the response back.
    """
    log.info("Processing conversion request")
    payload = data.get("payload")

    date = payload.get("date")
    stake = payload.get("stake")
    currency = payload.get("currency")

    try:
        euro_exchnage_rate = await fetch_exchange_rate(date=date, currency=currency)
    except ExchangeRateError as e:
        await connection.send(
            json.dumps(
                {
                    "type": "error",
                    "id": data.get("id"),
                    "message": f"Unable to convert stake. Error: {e}",
                },
            ),
        )
        log.warning("Error response message sent")
        return

    log.debug("Fetched exchange rate: %s", euro_exchnage_rate)

    data["date"] = pendulum.now().to_iso8601_string()
    data["payload"]["stake"] = round(stake * euro_exchnage_rate.rate, ndigits=5)
    data["payload"]["currency"] = "EUR"

    await connection.send(json.dumps(data))
    log.info("Success response message sent")


async def simple_currency_service() -> None:
    """
    Connect to the web socket server and handle incoming messages.
    """
    while True:
        background_tasks: set[asyncio.Task] = set()

        try:
            log.info("Attempting to connect to %s", WSS_URI)
            async with websockets.connect(WSS_URI) as connection:
                log.info("Successfully connected to %s", WSS_URI)
                # Schedule the task within the event loop
                heartbeat_task = asyncio.create_task(send_heartbeat_periodically(connection))

                while True:
                    message = await asyncio.wait_for(
                        connection.recv(),
                        timeout=HEARTBEAT_THRESHOLD_SECONDS,
                    )
                    data: JSONObject = json.loads(message)

                    message_type = data.get("type")
                    match message_type:
                        case "heartbeat":
                            log.info("Heartbeat received")
                        case "message":
                            # Schedule the task within the event loop
                            task = asyncio.create_task(process_conversion_request(connection, data))
                            background_tasks.add(task)
                            task.add_done_callback(background_tasks.discard)
                        case "error":
                            log.error("Error received: %s", message)
                        case _:
                            log.warning("Unknown message type: %s", message_type)

        # Continue and refresh the connection
        except TimeoutError:
            log.warning("Heartbeat timeout")

        finally:
            log.debug("Cleaning up spawned tasks")
            heartbeat_task.cancel()

            for task in background_tasks:
                log.debug("Cancelling task: %s", task)
                task.cancel()

            await connection.close()


def setup_logging() -> None:
    """
    Set up logging configuration.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=log_format, level=logging.INFO, datefmt=date_format)
    # Suppress httpx logs
    httpx_log = logging.getLogger("httpx")
    httpx_log.setLevel(logging.ERROR)


def main() -> None:
    """
    Entry point for the currency conversion service.
    """
    setup_logging()
    dotenv.load_dotenv()
    asyncio.run(simple_currency_service())


if __name__ == "__main__":
    main()
