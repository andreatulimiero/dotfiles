return require('packer').startup(function(use)
  use 'wbthomason/packer.nvim'
  use {
    'nvim-telescope/telescope.nvim', tag = '0.1.1',
    requires = { {'nvim-lua/plenary.nvim'} }
  }
  use { "ellisonleao/gruvbox.nvim" }
  use('nvim-treesitter/nvim-treesitter', {run = ':TSUpdate'})
  use {
    'VonHeikemen/lsp-zero.nvim',
    branch = 'v2.x',
    requires = {
      {'neovim/nvim-lspconfig'},
      {
        'williamboman/mason.nvim',
        run = function()
          pcall(vim.cmd, 'MasonUpdate')
        end,
      },
      {'williamboman/mason-lspconfig.nvim'},
      {'hrsh7th/nvim-cmp'},
      {'hrsh7th/cmp-nvim-lsp'},
      {'L3MON4D3/LuaSnip'},
    }
  }
  use {
    'Exafunction/codeium.vim',
    config = function ()
      vim.keymap.set('i', '<C-t>', function () return vim.fn['codeium#Accept']() end, { expr = true })
    end
  }
  use {
    "kelly-lin/ranger.nvim",
    config = function()
      require("ranger-nvim").setup({ replace_netrw = true })
      vim.api.nvim_set_keymap("n", "<C-n>", "", {
        noremap = true,
        callback = function()
          require("ranger-nvim").open(true)
        end,
      })
    end,
  }
  use {
    'LukasPietzschmann/telescope-tabs',
    requires = { 'nvim-telescope/telescope.nvim' }
  }
  use {
    "kelly-lin/telescope-ag",
    dependencies = { "nvim-telescope/telescope.nvim" },
  }
end)

