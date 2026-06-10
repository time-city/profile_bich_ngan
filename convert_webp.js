const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const assetDir = path.join(__dirname, 'asset');

function walkSync(currentDirPath, callback) {
    fs.readdirSync(currentDirPath).forEach(function (name) {
        var filePath = path.join(currentDirPath, name);
        var stat = fs.statSync(filePath);
        if (stat.isFile()) {
            callback(filePath, stat);
        } else if (stat.isDirectory()) {
            walkSync(filePath, callback);
        }
    });
}

const filesToProcess = [];

walkSync(assetDir, function(filePath) {
    if (filePath.match(/\.(jpg|jpeg|png|heic|JPG)$/i)) {
        filesToProcess.push(filePath);
    }
});

console.log(`Found ${filesToProcess.length} images to convert.`);

async function processImages() {
    for (const filePath of filesToProcess) {
        const ext = path.extname(filePath);
        const dirname = path.dirname(filePath);
        const basename = path.basename(filePath, ext);
        const newPath = path.join(dirname, basename + '.webp');
        
        try {
            // console.log(`Converting ${basename}${ext} to WebP...`);
            await sharp(filePath)
                .resize({ width: 1200, withoutEnlargement: true }) // Scale down to max 1200px width
                .webp({ quality: 80 }) // 80% quality for good balance
                .toFile(newPath);
                
            // Delete original file after successful conversion to save space
            fs.unlinkSync(filePath);
        } catch (err) {
            console.error(`Failed to process ${filePath}:`, err);
        }
    }
    console.log('All images converted to WebP successfully!');
}

processImages();
