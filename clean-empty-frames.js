const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const projectsDir = path.join(__dirname, 'src/components/projects');
const files = fs.readdirSync(projectsDir).filter(f => f.startsWith('project-') && f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(projectsDir, file);
  let html = fs.readFileSync(filePath, 'utf8');

  // We only care about files with bento-gallery-6
  if (!html.includes('bento-gallery-6')) continue;

  const dom = new JSDOM(html);
  const document = dom.window.document;

  const bentoGallery = document.querySelector('.bento-gallery-6');
  if (!bentoGallery) continue;

  const items = bentoGallery.querySelectorAll('.gallery-item.bento-item');
  let hasEmpty = false;
  
  items.forEach(item => {
    const img = item.querySelector('img');
    if (img && img.getAttribute('src') === '') {
      hasEmpty = true;
      item.remove(); // Delete the empty frame
    }
  });

  if (hasEmpty) {
    // Check how many items are left
    const remainingItems = bentoGallery.querySelectorAll('.gallery-item.bento-item');
    if (remainingItems.length === 5) {
      bentoGallery.classList.remove('bento-gallery-6');
      bentoGallery.classList.add('bento-gallery-5');
    }
    
    fs.writeFileSync(filePath, document.body.innerHTML, 'utf8');
    console.log(`Deleted empty frame and updated to bento-gallery-5 in ${file}`);
  }
}
