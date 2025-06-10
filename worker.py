import requests
import yaml

# Download the original configuration file
url = "https://raw.githubusercontent.com/aiboboxx/clashfree/refs/heads/main/clash.yml"
response = requests.get(url)
content = response.text

# Clean up HTML tags
header_tag = '<pre style="word-wrap: break-word; white-space: pre-wrap;">'
footer_tag = '</pre>'

if content.startswith(header_tag):
    content = content[len(header_tag):]
if content.endswith(footer_tag):
    content = content[:-len(footer_tag)]

# Parse YAML
data = yaml.safe_load(content)

# Remove proxies with type 'ss' and record their names
removed_names = []
if 'proxies' in data:
    # Filter out proxies of type 'ss'
    filtered_proxies = []
    for proxy in data['proxies']:
        if proxy.get('type') == 'ss':
            # Decode Unicode escape sequences to actual characters
            name = proxy['name'].encode('utf-8').decode('unicode_escape')
            removed_names.append(name)
        else:
            filtered_proxies.append(proxy)
    data['proxies'] = filtered_proxies

# Convert YAML to text lines
yaml_text = yaml.dump(data, allow_unicode=True)
lines = yaml_text.splitlines()

# Filter out lines containing removed names (handling Unicode escape sequences)
filtered_lines = []
for line in lines:
    # Decode Unicode escape sequences in the line
    decoded_line = line.encode('utf-8').decode('unicode_escape')
    # Check if it contains any removed names
    if not any(name in decoded_line for name in removed_names):
        filtered_lines.append(line)

# Save the final result
with open('clash.yaml', 'w', encoding='utf-8') as f:
    f.write("\n".join(filtered_lines))

print(f"Processing completed! Removed {len(removed_names)} SS proxies")
print(f"Saved as: clash.yaml")
