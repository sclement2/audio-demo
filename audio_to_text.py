import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

openai = AsyncOpenAI()


async def transcribe_audio(audio_filename="audio.wav"):
    audio_file = await asyncio.to_thread(open, audio_filename, "rb")
    stream = await openai.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
        response_format="text",
        stream=True,
    )
    transcript = ""
    async for event in stream:
        if event.type == "transcript.text.delta":
            print(event.delta, end="", flush=True)
            transcript += event.delta
    print()
    audio_file.close()
    return transcript


def main():
    try:
        loop = asyncio.get_running_loop()  # Check if a loop is already running
    except RuntimeError:
        loop = asyncio.new_event_loop()  # Create a new event loop if none exists
        asyncio.set_event_loop(loop)
    loop.run_until_complete(transcribe_audio("sample-4.mp3"))


if __name__ == "__main__":
    main()
