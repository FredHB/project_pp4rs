# this makes execution stop on errors
set -e

# remove the directory if it exists and start from scratch
rm -rf ./dist
mkdir dist
mkdir dist/out/
mkdir dist/src/
mkdir dist/src/doc/

# copy all html and png outfiles into the dist folder (use update option)
cp out/*.html dist/out/ -u
cp out/*.png dist/out/ -u
# copy index.html
# but for this to work, the relative paths in the html need to change becaus dist is root
sed 's+src[ ]*=[ ]*\"..\/..\/+src="./+g' src/doc/index.html > dist/index.html

# change to the publish folder and init a new git repo
cd dist
git init --initial-branch=main
git add -A
git commit -m 'Deploy to GH pages'

# force push to the gh-pages branch
git push -f git@github.com:FredHB/project_pp4rs.git main:gh-pages

# go back and delete everything
# (this is optional, you can also keep your folder locally)
# (in you do so )
cd ..
rm -rf ./dist 