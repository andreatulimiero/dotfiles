"   _    _      _               _       _ _ 
"  | |  | |    (_)             | |     | | |
"  | |__| | ___ _ _ __ ___   __| | __ _| | |
"  |  __  |/ _ \ | '_ ` _ \ / _` |/ _` | | |
"  | |  | |  __/ | | | | | | (_| | (_| | | |
"  |_|  |_|\___|_|_| |_| |_|\__,_|\__,_|_|_|
"                                          
"  Filename:  .vimrc
"  Github:    https://github.com/andreatulimiero/dotfiles
"  Mantainer: Andrea Tulimiero (Heimdall)

"Initial setup {{{
if empty(glob('~/.vim/autoload/plug.vim'))
silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
\ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
" }}}

"Indentation {{{
set shiftwidth=2
set tabstop=2
set softtabstop=2
set expandtab
" }}}

" Appearance {{{
set number
" set nu rnu
let &showbreak='↪ '
set breakindent
set background=dark
syntax on
set laststatus=2
" }}}

"Folding {{{
"set foldlevel=0
set foldmethod=marker
" }}}

" Search and Autocomplete {{{
set wildmenu
set incsearch
inoremap <C-n> <C-x><C-n>
" }}}

" Autoreload {{{
autocmd! bufwritepost .vimrc source %
" }}}

" Tabs {{{
nnoremap <C-l> :tabn<CR>
nnoremap <C-h> :tabp<CR>
" }}}

"Windows {{{
""Moving {{{
nnoremap h <C-W><C-H>
nnoremap j <C-W><C-J>
nnoremap k <C-W><C-K>
nnoremap l <C-W><C-L>
""}}}
"" Resizing {{{
nnoremap H :vertical resize -1<CR>
nnoremap J :resize +1<CR>
nnoremap K :resize -1<CR>
nnoremap L :vertical resize +1<CR>
"" }}}
"}}}

" Abbreviations {{{
" Search TODO/FIXME/XXX/NOTE
nnoremap <leader>t :Ag (TODO)\|(FIXME)\|(XXX)\|(NOTE)<CR>
" }}}

" Miscellanea {{{
" Replace word below cursor
nnoremap <leader>r :%s/\<<C-r><C-w>\>/
"set mouse=a
imap kj <Esc>
set exrc
set secure
" Avoid black lines when using vim with kitty
" let &t_ut=''
" Fix for backsapce
set bs=2
" Save in clipboard (and a file backup) and quit
nmap <leader>yq :w! /tmp/scratch.txt<CR>gg"+yG:q!<CR>
" Toggle dark/light
function! ToggleBackground()
  if &background == "dark"
    set background=light
    let g:airline_solarized_bg='light'
  else
    set background=dark
    let g:airline_solarized_bg='dark'
  endif
  runtime autoload/lightline/colorscheme/solarized.vim
  call lightline#init()
  call lightline#colorscheme()
  call lightline#update()
endfunction
nmap <leader>bg :call ToggleBackground()<CR>
" }}}

" Build&Run {{{
" Python {{{
au FileType python nnoremap <C-B> :!clear && python %<CR>
" au BufWritePost *.py call flake8#Flake8()
" }}}
" Go {{{
au FileType go nnoremap <C-B> :!clear && go run . %<CR>
" }}}
" LaTeX {{{
au FileType tex nnoremap <C-B> :!make <CR><CR>
" }}}
" }}}

" Plugins {{{
call plug#begin('~/.vim/plugged')
Plug 'scrooloose/nerdcommenter'
Plug 'scrooloose/nerdtree'
Plug 'markonm/traces.vim'
Plug 'itchyny/lightline.vim'
Plug 'altercation/vim-colors-solarized'
Plug 'sainnhe/edge'
Plug 'lervag/vimtex'
Plug 'tpope/vim-fugitive'
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
Plug 'majutsushi/tagbar'
Plug 'aserebryakov/vim-todo-lists'
Plug 'xolox/vim-misc'
Plug 'xolox/vim-notes'
call plug#end()

" NERDCommenter {{{
let g:NERDSpaceDelims = 1
let g:NERDAltDelims_c = 1
" }}}

" Nerdtree {{{
map <C-n> :NERDTreeToggle<CR>
let g:NERDTreeDirArrowExpandable = '+'
let g:NERDTreeDirArrowCollapsible = '-'
"" }}}

" Solarized {{{
let g:solarized_termcolors=256
colorscheme solarized
"" }}}

" Edge {{{
" set termguicolors
" colorscheme edge
let g:neon_popup_menu_selection_background = 'green'
"" }}}

""{{{ VimAirline
let g:lightline = {
      \ 'colorscheme': 'solarized',
      \ }
let g:airline_solarized_bg='dark'
if !has('gui_running')
  set t_Co=256
endif
""}}}

" {{{ Fzf
let $FZF_DEFAULT_COMMAND = 'ag -g ""'
nnoremap <C-p> :Files<CR>
" }}}

" Ag {{{
nmap <C-\> :Ag <C-R><C-W><CR>
" }}}

" Tagbar {{{
" Open Tagbar and jump into it, or close it already open
function! ToggleTagbar()
    let tagbar_open = bufwinnr('__Tagbar__') != -1
    if tagbar_open
        TagbarClose
    else
        TagbarOpen f
    endif
endfunction
nnoremap <C-t> :call ToggleTagbar() <CR>
" }}}

" Vimtex {{{
let g:tex_flavor = 'LaTeX'
let g:vimtex_view_method = 'zathura'
let g:vimtex_fold_enabled = 1
let g:vimtex_compiler_latexmk = {
    \ 'options' : [
    \   '-pdf',
    \   '-shell-escape',
    \   '-verbose',
    \   '-file-line-error',
    \   '-synctex=1',
    \   '-interaction=nonstopmode',
    \ ],
    \}
" }}}

" TODO-Lists {{{
nnoremap <buffer> > :VimTodoListsIncreaseIndent<CR>
nnoremap <buffer> < :VimTodoListsDecreaseIndent<CR>
" }}}

" Vim Notes {{{
let g:notes_directories = ['~/Notes']
" }}}
" }}}

" Spellcheck {{{
" (placed here to override colorscheme defaults) 
set spelllang=en_us
hi SpellBad cterm=underline
nnoremap z= 1z=
" }}}
