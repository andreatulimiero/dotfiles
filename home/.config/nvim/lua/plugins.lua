return {
  "ellisonleao/gruvbox.nvim",
  "hrsh7th/nvim-cmp",
  {
    "nvim-telescope/telescope.nvim",
    version = "0.1.6",
    dependencies = { "nvim-lua/plenary.nvim" },
  },
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
  },
  {
    "mason-org/mason.nvim",
    opts = {}
  },
  {
    "mason-org/mason-lspconfig.nvim",
    opts = {
      ensure_installed = {
        "lua_ls", -- Lua
        "rust_analyzer", -- Rust
        "clangd", -- C++
        "pyright", -- Python
        "gopls" -- Golang
      },
    },
    dependencies = {
        {"mason-org/mason.nvim"},
        "neovim/nvim-lspconfig",
    },
  },
  {
    'saghen/blink.cmp',
    version = '1.*',
    ---@module 'blink.cmp'
    ---@type blink.cmp.Config
    opts = {
      keymap = {
        preset = 'none',
        ['<C-k>'] = { 'select_prev', 'fallback' },
        ['<C-j>'] = { 'select_next', 'fallback' },
        ['<C-f>'] = { 'accept', 'fallback' },
      },
      appearance = {
        nerd_font_variant = 'mono'
      },
      completion = { documentation = { auto_show = false } },
      sources = {
        default = { 'lsp', 'path', 'buffer' },
      },
      fuzzy = { implementation = "prefer_rust_with_warning" }
    },
    opts_extend = { "sources.default" }
  },
  {
    "LukasPietzschmann/telescope-tabs",
    dependencies = { "nvim-telescope/telescope.nvim" },
  },
  {
    "kelly-lin/telescope-ag",
    dependencies = { "nvim-telescope/telescope.nvim" },
  },
  {
    "folke/trouble.nvim",
    opts = {},
    cmd = "Trouble",
    keys = {
      {
        "<leader>xx",
        "<cmd>Trouble diagnostics toggle<cr>",
        desc = "Diagnostics (Trouble)",
      },
    }
  },
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {},
    keys = {
      {
        "<leader>?",
        function()
          require("which-key").show({ global = false })
        end,
        desc = "Buffer Local Keymaps (which-key)",
      },
    },
  },
  {
    'stevearc/conform.nvim',
    opts = {
      formatters_by_ft = {
        go = { "golines" },
        python = { "ruff" },
      },
      formatters = {
        golines = {
          prepend_args = function(ctx)
            return {
              "-m",
              "80",
              "--base-formatter=gofmt",
            }
          end,
        },
      },
      format_on_save = {
        timeout_ms = 5000,
        lsp_format = "never",
      },
    },
  },
  {
    "nickvandyke/opencode.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      -- NickvanDyke uses a global var, NOT setup()
      vim.g.opencode_opts = {
        -- auto-discovers opencode running in CWD via lsof/ss — no port needed
        -- as long as you start `opencode` in your project directory
      }
      vim.o.autoread = true -- reload files opencode edits on disk
      vim.keymap.set("n", "<C-s>", function()
        return require("opencode").operator("@file ")
      end, { expr = true, desc = "Send file to opencode" })
      vim.keymap.set({ "n", "x" }, "<C-s>", function()
        return require("opencode").operator("@this ")
      end, { expr = true, desc = "Add selection to opencode" })
    end,
  },
  {
    "sindrets/diffview.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    cmd = { "DiffviewOpen", "DiffviewClose", "DiffviewFileHistory" },
    keys = {
      { "<leader>dv", "<cmd>DiffviewOpen<cr>",          desc = "Diffview: all changes" },
      { "<leader>dc", "<cmd>DiffviewClose<cr>",         desc = "Diffview: close" },
      { "<leader>df", "<cmd>DiffviewFileHistory %<cr>", desc = "Diffview: this file" },
    },
    config = function()
      local actions = require("diffview.actions")
      require("diffview").setup({
        enhanced_diff_hl = true,
        keymaps = {
          file_panel = {
            { "n", "j", actions.select_next_entry, { desc = "Next file + open diff" } },
            { "n", "k", actions.select_prev_entry, { desc = "Prev file + open diff" } },
            { "n", "<cr>", actions.focus_entry, { desc = "Focus entry" } },
          },
        },
      })
    end,
  },
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
      require("gitsigns").setup({
        signs = { },
        signcolumn = false,
        on_attach = function(buf)
          local gs = require("gitsigns")
          local map = function(mode, lhs, rhs, desc)
            vim.keymap.set(mode, lhs, rhs, { buffer = buf, desc = desc })
          end
          map("n", "]h", function() gs.nav_hunk("next") end, "Next hunk")
          map("n", "[h", function() gs.nav_hunk("prev") end, "Prev hunk")
          map("n", "<leader>ha", gs.stage_hunk, "Accept hunk")
          map("v", "<leader>ha", function()
            gs.stage_hunk({ vim.fn.line("."), vim.fn.line("v") })
          end, "Accept selected lines")
          map("n", "<leader>hr", gs.reset_hunk, "Reject hunk")
          map("v", "<leader>hr", function()
            gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") })
          end, "Reject selected lines")
          map("n", "<leader>hR", gs.reset_buffer, "Reject all in file")
        end,
      })
    end,
  },
}
