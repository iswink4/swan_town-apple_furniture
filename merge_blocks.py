import json

# 读取main版本
with open('A04da90a2dc7f464b90982fecedb72818R/blocks.json', 'r', encoding='utf-8-sig') as f:
    main_blocks = json.load(f)

# 读取netease版本
with open('netease_blocks_temp.json', 'r', encoding='utf-8-sig') as f:
    netease_blocks = json.load(f)

# 统计
main_count = len(main_blocks) - 1
print(f'main分支方块数量: {main_count}')

# 提取新增方块
new_blocks = {k: v for k, v in netease_blocks.items() if k.startswith('swan_town_apple:')}
print(f'新增方块数量: {len(new_blocks)}')

# 合并
main_blocks.update(new_blocks)
print(f'合并后方块总数: {len(main_blocks) - 1}')

# 保存
with open('A04da90a2dc7f464b90982fecedb72818R/blocks.json', 'w', encoding='utf-8') as f:
    json.dump(main_blocks, f, ensure_ascii=False, indent=4)

print('✅ blocks.json合并完成')