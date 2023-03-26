# Ravencoin Discord Bot
 This is a Python-based Discord bot that fetches the current price and statistics for Ravencoin and posts it in an embedded message in a specific channel. Additionally, it sets the bot's activity to display the current Ravencoin price and offers the option to name a voice or text channel with the current price.

## Installation

> 1. Clone the repository and navigate to the project directory.
```
git clone https://github.com/your-username/RBHZ_RVN_Discord_Metrics.git
```
```
cd RBHZ_RVN_Discord_Metrics
```

> 2. Create a `.env` file and add the following environment variables:
```
TOKEN=<your_discord_bot_token_here>
EMBED_ID=<embed_channel_id>
CHANNEL_ID=<channel_id>
UPDATE_INTERVAL=<update_interval_in_seconds>
THUMBNAIL_URL=<thumbnail_image_url>
IMAGE_URL=<image_url>
AUTHOR_URL=<author_image_url>
DESCRIPTION=<embed_description>
WEBSITE_LINK=<website_link>
```
Replace each value with your own values.

> 3. Run INSTALL.bat to install the bot
> 4. Run LAUNCH.bat to start the bot.

## Configuration

### Environment Variables

| Variable        | Description |
| --------------- | ----------- |
| TOKEN           | Your Discord bot token. |
| EMBED_ID        | The ID of the channel where you want the Ravencoin statistics embedded message sent. |
| CHANNEL_ID      | The ID of the channel where you want the Ravencoin statistics channel name to be updated. |
| UPDATE_INTERVAL | The interval (in seconds) at which you want to update the Ravencoin statistics. |
| THUMBNAIL_URL   | The URL of the thumbnail image to use in the embedded message. |
| IMAGE_URL       | The URL of the image to use in the embedded message. |
| AUTHOR_URL      | The URL of the author image to use in the embedded message. |
| DESCRIPTION     | The description to use in the embedded message. |
| WEBSITE_LINK    | The link to website. |

## Usage
Once the bot is running, it will automatically update the Ravencoin statistics at the specified interval and post it in the specified channel.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE). This license is a copyleft license that requires any modifications or derivatives of the code to be released under the same license. You can read more about the terms of the license on the [GNU website](https://www.gnu.org/licenses/gpl-3.0.en.html).
