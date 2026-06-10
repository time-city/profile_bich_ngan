const fs = require('fs');
const path = require('path');

const assetDir = path.join(__dirname, 'asset');

let eventsData = [];
let eventIdCounter = 1;

function getImages(dir) {
    let results = [];
    try {
        fs.readdirSync(dir).forEach(function(file) {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);
            if (stat && !stat.isDirectory()) {
                if (file.match(/\.(jpg|jpeg|png|gif|HEIC|heic|JPG|webp)$/i)) {
                    // Normalize path for web (forward slashes)
                    const relPath = './' + path.relative(__dirname, fullPath).replace(/\\/g, '/');
                    results.push(relPath);
                }
            }
        });
    } catch(e) {
        console.error(e);
    }
    return results;
}

// Read categories
const categories = fs.readdirSync(assetDir).filter(f => {
    return fs.statSync(path.join(assetDir, f)).isDirectory();
});

categories.forEach(category => {
    const categoryPath = path.join(assetDir, category);
    const events = fs.readdirSync(categoryPath).filter(f => {
        return fs.statSync(path.join(categoryPath, f)).isDirectory();
    });
    
    events.forEach(eventName => {
        const eventPath = path.join(categoryPath, eventName);
        const images = getImages(eventPath);
        
        if (images.length > 0) {
            eventsData.push({
                id: `event-${eventIdCounter++}`,
                title: eventName,
                category: category,
                // A default brief based on the folder name, user can customize later
                brief: `Một trong những sự kiện nổi bật thuộc mảng ${category}. MC Bích Ngân đã dẫn dắt thành công chương trình "${eventName}", mang lại những khoảnh khắc đáng nhớ và chuyên nghiệp.`,
                images: images
            });
        }
    });
});

const output = `const eventsData = ${JSON.stringify(eventsData, null, 2)};\n\n// Export for use if needed in modules, though in vanilla JS script tag inclusion, it acts as a global variable.\nwindow.EVENTS_DATA = eventsData;\n`;

fs.writeFileSync(path.join(__dirname, 'data.js'), output);
console.log(`data.js generated successfully with ${eventsData.length} events!`);
