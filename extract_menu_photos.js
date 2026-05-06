/**
 * extract_menu_photos.js
 * 从 Ang Success Enterprise 菜单 PNG 中裁剪出每个商品的照片
 * 输出为独立的 JPG 文件 + 生成菜单数据
 */
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const SRC_IMG = path.resolve(__dirname, 'Food Menu Special Price.png');
const OUT_DIR = path.join(__dirname, 'menu_photos');

// 菜单原图中每个商品照片的大致位置 (基于视觉分析)
// 格式: { id, name, crop: { left, top, width, height } }
// 坐标基于原始图片尺寸 (约 700x1100)
// Image size: 1294 x 2000
const ITEMS = [
  {
    id: 'pancake',
    name: '曼煎糕 Pan Cake',
    crop: { left: 25, top: 90, width: 310, height: 220 }
  },
  {
    id: 'peanut-mochi',
    name: '花生麻糬 Peanut Mochi',
    crop: { left: 20, top: 320, width: 315, height: 220 }
  },
  {
    id: 'snow-mochi',
    name: '雪媚娘 Snow Mochi',
    crop: { left: 20, top: 545, width: 325, height: 230 }
  },
  {
    id: 'egg-tart',
    name: '葡式蛋挞 Portuguese Egg Tarts',
    crop: { left: 30, top: 880, width: 305, height: 220 }
  }
];

async function main() {
  console.log('Loading source image:', SRC_IMG);
  const img = sharp(SRC_IMG);
  const metadata = await img.metadata();
  console.log('Image size:', metadata.width, 'x', metadata.height);

  // Create output directory
  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  const results = [];

  for (const item of ITEMS) {
    const outPath = path.join(OUT_DIR, `${item.id}.jpg`);
    console.log(`\nCropping: ${item.name}`);
    console.log(`  Crop region: ${JSON.stringify(item.crop)}`);

    try {
      await img
        .clone()
        .extract({
          left: Math.round(item.crop.left),
          top: Math.round(item.crop.top),
          width: Math.round(item.crop.width),
          height: Math.round(item.crop.height)
        })
        .jpeg({ quality: 90 })
        .toFile(outPath);

      const stat = fs.statSync(outPath);
      console.log(`  ✅ Saved: ${outPath} (${(stat.size / 1024).toFixed(1)}KB)`);

      // Read as base64 for embedding
      const b64 = fs.readFileSync(outPath, 'base64');
      results.push({
        ...item,
        filePath: outPath,
        base64: `data:image/jpeg;base64,${b64}`,
        fileSize: stat.size
      });
    } catch (err) {
      console.error(`  ❌ Error cropping ${item.name}:`, err.message);
    }
  }

  // Generate menu data JS file for the Web App
  const menuData = generateMenuData(results);
  const menuDataPath = path.join(__dirname, 'ang_success_menu_data.js');
  fs.writeFileSync(menuDataPath, menuData, 'utf-8');
  console.log(`\n✅ Menu data saved to: ${menuDataPath}`);

  // Also save a JSON version
  const jsonPath = path.join(__dirname, 'ang_success_menu.json');
  const jsonData = results.map(r => ({
    id: r.id,
    name: r.name,
    image: r.base64,
    _filePath: r.filePath
  }));
  fs.writeFileSync(jsonPath, JSON.stringify(jsonData, null, 2), 'utf-8');
  console.log(`✅ JSON data saved to: ${jsonPath}`);

  console.log('\nDone! Extracted', results.length, 'product photos.');
}

function generateMenuData(items) {
  // Build the complete menu for Ang Success Enterprise
  const menuItems = [
    // 曼煎糕 Pan Cake - two variants
    {
      id: 'as_pan_cake_pandan',
      name: '曼煎糕 (班兰) Pan Cake Pandan',
      emoji: '🥞',
      price: 1.60,
      category: 'Traditional Cakes',
      desc: '香浓班兰味曼煎糕，一片',
      image: items.find(i => i.id === 'pancake')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_pan_cake_brownsugar',
      name: '曼煎糕 (黑糖) Pan Cake Brown Sugar',
      emoji: '🥞',
      price: 1.60,
      category: 'Traditional Cakes',
      desc: '黑糖味曼煎糕，一片',
      image: items.find(i => i.id === 'pancake')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_pan_cake_box',
      name: '曼煎糕 一盒 (11片) Big Plate',
      emoji: '📦',
      price: 16.00,
      category: 'Traditional Cakes',
      desc: '整盒曼煎糕，11片装',
      image: items.find(i => i.id === 'pancake')?.base64 || null,
      promoPrice: null
    },
    // 花生麻糬 Peanut Mochi
    {
      id: 'as_peanut_mochi',
      name: '花生麻糬 Peanut Mochi (一盒)',
      emoji: '🥜',
      price: 5.50,
      category: 'Mochi',
      desc: '原味花生麻糬，香甜软糯',
      image: items.find(i => i.id === 'peanut-mochi')?.base64 || null,
      promoPrice: null
    },
    // 雪媚娘 Snow Mochi - RM 4.50 variants
    {
      id: 'as_snow_mochi_mango',
      name: '雪媚娘 Snow Mochi (芒果)',
      emoji: '🥭',
      price: 4.50,
      category: 'Mochi',
      desc: '新鲜芒果馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_oreo',
      name: '雪媚娘 Snow Mochi (奥利奥)',
      emoji: '🍪',
      price: 4.50,
      category: 'Mochi',
      desc: '奥利奥风味雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_banana_choco',
      name: '雪媚娘 Snow Mochi (香蕉巧克力)',
      emoji: '🍫',
      price: 4.50,
      category: 'Mochi',
      desc: '香蕉巧克力馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_brown_sugar',
      name: '雪媚娘 Snow Mochi (黑糖珍珠)',
      emoji: '🧋',
      price: 4.50,
      category: 'Mochi',
      desc: '黑糖珍珠馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    // 雪媚娘 Snow Mochi - RM 5.00 variants
    {
      id: 'as_snow_mochi_icecream',
      name: '雪媚娘 Snow Mochi (冰淇淋)',
      emoji: '🍨',
      price: 5.00,
      category: 'Mochi',
      desc: '冰淇淋馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_longan',
      name: '雪媚娘 Snow Mochi (龙眼)',
      emoji: '👁️',
      price: 5.00,
      category: 'Mochi',
      desc: '新鲜龙眼馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_strawberry',
      name: '雪媚娘 Snow Mochi (草莓)',
      emoji: '🍓',
      price: 5.00,
      category: 'Mochi',
      desc: '新鲜草莓馅雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    {
      id: 'as_snow_mochi_choco_chips',
      name: '雪媚娘 Snow Mochi (巧克力豆)',
      emoji: '🍫',
      price: 5.00,
      category: 'Mochi',
      desc: '巧克力豆雪媚娘',
      image: items.find(i => i.id === 'snow-mochi')?.base64 || null,
      promoPrice: null
    },
    // 葡式蛋挞 Portuguese Egg Tarts
    {
      id: 'as_egg_tart',
      name: '葡式蛋挞 Portuguese Egg Tart (一粒)',
      emoji: '🥧',
      price: 3.50,
      category: 'Pastries',
      desc: '酥脆外皮，嫩滑蛋心，经典葡式蛋挞',
      image: items.find(i => i.id === 'egg-tart')?.base64 || null,
      promoPrice: null
    }
  ];

  return `/**
 * Ang Success Enterprise - Menu Data
 * Generated from Food Menu Special Price.png
 * Generated at: ${new Date().toISOString()}
 * 
 * Usage: In browser console or via script tag:
 *   DB.saveMenu(ANG_SUCCESS_MENU);
 */

const ANG_SUCCESS_MENU = ${JSON.stringify(menuItems, null, 2)};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ANG_SUCCESS_MENU;
}
`;
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
