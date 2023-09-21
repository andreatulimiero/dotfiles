-- Indentation And Formatting
vim.opt.shiftwidth = 2
vim.opt.tabstop=2
vim.opt.softtabstop=2
vim.opt.expandtab = true
-- vim.opt.nojoinspaces = true

-- Search
vim.opt.incsearch = true
vim.opt.hlsearch = false;

-- Appearance
vim.opt.number = true
vim.opt.breakindent = true
vim.opt.showbreak = "↪ "
vim.opt.colorcolumn = "81"
vim.opt.scrolloff = 4

-- Misc
vim.opt.undofile = true
vim.keymap.set("i", "kj", "<Esc>")

-- Tabs
vim.keymap.set("n", "<C-h>", ":tabp<CR>")
vim.keymap.set("n", "<C-l>", ":tabn<CR>")
