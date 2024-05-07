-- Mason setup
local success, err = pcall(function() require('mason').setup() end)
if not success then
  print("Mason not found, aborting lsp.lua execution")
  return
end
require('mason-lspconfig').setup {
	ensure_installed = {
		"lua_ls", -- Lua
		"rust_analyzer", -- Rust
		"clangd", -- C++
		"pyright" -- Python
	},
}

-- LSP-Zero setup
local lsp = require('lsp-zero')
lsp.preset('recommended')
local cmp = require('cmp')
cmp.setup {
  experimental = {
    ghost_text = true
  },
  sources = {
    -- { name = "codeium" },
    { name = "nvim_lsp" },
    { name = "buffer", keyword_length = 3}
  }
}
local cmp_select = { behavior = cmp.SelectBehavior.Select }
local cmp_mappings = lsp.defaults.cmp_mappings({
	['<C-k>'] = cmp.mapping.select_prev_item(cmp_select),
	['<C-j>'] = cmp.mapping.select_next_item(cmp_select),
	['<C-f>'] = cmp.mapping.confirm({ select = true }),
})
lsp.setup_nvim_cmp({ mapping = cmp_mappings })
lsp.setup()

-- Setup language servers
require('lspconfig').lua_ls.setup {
	settings = {
		Lua = {
			diagnostics = {
				globals = {'vim'}
			}
		}
	}
}
vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('UserLspConfig', {}),
  callback = function(ev)
    -- Enable completion triggered by <c-x><c-o>
    vim.bo[ev.buf].omnifunc = 'v:lua.vim.lsp.omnifunc'

    local opts = { buffer = ev.buf }
    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, opts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', '<leader>r', vim.lsp.buf.rename, opts)
    vim.keymap.set({ 'n', 'v' }, '<leader>ca', vim.lsp.buf.code_action, opts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
    vim.keymap.set('n', '<leader>f', function()
      vim.lsp.buf.format { async = true }
    end, opts)
  end,
})
