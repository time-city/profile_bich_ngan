#!/bin/bash
cd /Users/admin/Documents/profile_bich_ngan

# Extract footer to 9-footer.html
awk '/<footer/{flag=1} flag; /<\/footer>/{flag=0}' src/sections/7-partners-footer.html > src/sections/9-footer.html

# Remove footer from 7-partners-footer.html and save to 7-partners.html
awk '/<footer/{flag=1} !flag; /<\/footer>/{flag=0}' src/sections/7-partners-footer.html > src/sections/7-partners.html

rm src/sections/7-partners-footer.html
