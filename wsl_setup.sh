bash # enter wsl
whoami

# prerequisites
sudo apt-get install ruby-full build-essential zlib1g-dev

# set up a gem installation directory for your user account
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# install Jekyll and Bundler
gem install jekyll bundler

# check
ruby -v
gem -v
gcc -v
make -v
jekyll -v

# dependencie
bundle install

# fix uncompatible issue of Ruby 3.0+ and pathutil
# refer: https://stackoverflow.com/questions/66113639/jekyll-serve-throws-no-implicit-conversion-of-hash-into-integer-error/67580565#67580565:~:text=Apply%20the%20patch%20to%20pathutil
sudo sed -i.bak 's/, kwd/, **kwd/' $(gem which pathutil)
bundle add webrick
