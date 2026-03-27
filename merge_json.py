# -*- coding: utf-8 -*-
"""
合并blocks.json和terrain_texture.json文件
从netease分支提取新增的re/相关资源，合并到main版本中
"""
import json
import os

def merge_blocks_json():
    """合并blocks.json文件"""
    print("开始合并 blocks.json...")
    
    # 读取当前版本（main分支）的blocks.json
    main_blocks_path = "A04da90a2dc7f464b90982fecedb72818R/blocks.json"
    with open(main_blocks_path, 'r', encoding='utf-8-sig') as f:
        main_blocks = json.load(f)
    
    # 从git读取netease分支的blocks.json
    import subprocess
    result = subprocess.run(
        ['git', 'show', 'origin/netease:A04da90a2dc7f464b90982fecedb72818R/blocks.json'],
        capture_output=True,
        text=True,
        encoding='utf-8-sig'
    )
    netease_blocks = json.loads(result.stdout)
    
    # 统计原始数量
    main_count = len(main_blocks) - 1  # 减去format_version
    print(f"main分支方块数量: {main_count}")
    
    # 提取netease中所有swan_town_apple:开头的方块
    new_blocks = {}
    for key, value in netease_blocks.items():
        if key.startswith('swan_town_apple:'):
            new_blocks[key] = value
    
    print(f"新增方块数量: {len(new_blocks)}")
    
    # 将新增方块追加到main版本中
    # 在最后一个placeholder之后添加
    last_key = list(main_blocks.keys())[-1]  # placeholder_wall_bottom
    
    # 创建新的合并后的字典
    merged_blocks = {}
    for key, value in main_blocks.items():
        merged_blocks[key] = value
        if key == last_key:
            # 在最后一个placeholder后添加新增方块
            for new_key, new_value in new_blocks.items():
                merged_blocks[new_key] = new_value
    
    # 写入合并后的文件
    with open(main_blocks_path, 'w', encoding='utf-8') as f:
        json.dump(merged_blocks, f, ensure_ascii=False, indent=4)
    
    print(f"✅ blocks.json合并完成，总计: {len(merged_blocks) - 1}个方块")

def merge_terrain_texture_json():
    """合并terrain_texture.json文件"""
    print("\n开始合并 terrain_texture.json...")
    
    # 读取当前版本的terrain_texture.json
    main_terrain_path = "A04da90a2dc7f464b90982fecedb72818R/textures/terrain_texture.json"
    with open(main_terrain_path, 'r', encoding='utf-8-sig') as f:
        main_terrain = json.load(f)
    
    # 从git读取netease分支的terrain_texture.json
    import subprocess
    result = subprocess.run(
        ['git', 'show', 'origin/netease:A04da90a2dc7f464b90982fecedb72818R/textures/terrain_texture.json'],
        capture_output=True,
        text=True,
        encoding='utf-8-sig'
    )
    netease_terrain = json.loads(result.stdout)
    
    # 统计原始数量
    main_texture_count = len(main_terrain.get('texture_data', {}))
    print(f"main分支纹理数量: {main_texture_count}")
    
    # 提取netease中所有swan_town_apple:和re/相关的纹理
    new_textures = {}
    if 'texture_data' in netease_terrain:
        for key, value in netease_terrain['texture_data'].items():
            if key.startswith('swan_town_apple:') or 'textures/re/' in str(value):
                new_textures[key] = value
    
    print(f"新增纹理数量: {len(new_textures)}")
    
    # 合并纹理数据
    if 'texture_data' not in main_terrain:
        main_terrain['texture_data'] = {}
    
    # 将新增纹理添加到main版本中
    for key, value in new_textures.items():
        main_terrain['texture_data'][key] = value
    
    # 写入合并后的文件
    with open(main_terrain_path, 'w', encoding='utf-8') as f:
        json.dump(main_terrain, f, ensure_ascii=False, indent=4)
    
    print(f"✅ terrain_texture.json合并完成，总计: {len(main_terrain['texture_data'])}个纹理")

if __name__ == '__main__':
    try:
        merge_blocks_json()
        merge_terrain_texture_json()
        print("\n🎉 所有JSON文件合并完成！")
    except Exception as e:
        print(f"\n❌ 合并失败: {e}")
        import traceback
        traceback.print_exc()