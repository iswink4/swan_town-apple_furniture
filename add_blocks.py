import json
import io

# Read model list
with io.open('model_list.txt', 'r', encoding='utf-8') as f:
    models = [line.strip() for line in f if line.strip()]

# Read existing blocks.json
with io.open('A04da90a2dc7f464b90982fecedb72818R/blocks.json', 'r', encoding='utf-8') as f:
    content = f.read()
    # Remove BOM
    if content.startswith(u'\ufeff'):
        content = content[1:]
    blocks = json.loads(content)

# Add new configurations
count = 0
for model in models:
    key = 'swan_town_apple:{}'.format(model)
    if key not in blocks:
        blocks[key] = {
            'client_entity': {
                'block_icon': 'swan_town_apple:{}_icon'.format(model),
                'hand_model_use_client_entity': True,
                'identifier': 'swan_town_apple:{}'.format(model)
            },
            'sound': 'wood'
        }
        count += 1

# Write back to file
with io.open('A04da90a2dc7f464b90982fecedb72818R/blocks.json', 'w', encoding='utf-8') as f:
    json.dump(blocks, f, indent=4, ensure_ascii=False)
    f.write('\n')

print('Added {} new model configurations, total {} configurations'.format(count, len(blocks)))
