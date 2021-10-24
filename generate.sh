# Locating Working Directory
cd /home/xavierwah/xavierwah.xyz

# Compiling Static Website
echo "Starting building the site."
hexo clean
hexo generate

# Integrating Files
echo "Creating cache directory."
sudo mkdir .cache
sudo mkdir .cache/.git
echo "Integrating files."
sudo cp public/* .cache/ -r
sudo cp /mnt/c/Users/XavierWah/Documents/Github/Shelter/.git/* .cache/.git/ -r
echo "Updating Git folder."
sudo rm /mnt/c/Users/XavierWah/Documents/Github/Shelter/* -rf
sudo cp .cache/* /mnt/c/Users/XavierWah/Documents/Github/Shelter/ -r
echo "Removing cache directory."
sudo rm .cache -rf
echo "Site generated."
