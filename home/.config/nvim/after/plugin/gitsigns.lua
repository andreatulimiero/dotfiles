require("gitsigns").setup({
  signs = { },
  signcolumn = false,
  on_attach = function(buf)
    local gs = require("gitsigns")
    local map = function(mode, lhs, rhs, desc)
      vim.keymap.set(mode, lhs, rhs, { buffer = buf, desc = desc })
    end
    map("n", "gj", function() gs.nav_hunk("next") end, "Next hunk")
    map("n", "gk", function() gs.nav_hunk("prev") end, "Prev hunk")
    map("n", "gh", gs.stage_hunk, "Accept hunk")
    map("v", "gh", function()
      gs.stage_hunk({ vim.fn.line("."), vim.fn.line("v") })
    end, "Accept selected lines")
    map("n", "gH", gs.reset_hunk, "Reject hunk")
    map("v", "gH", function()
      gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") })
    end, "Reject selected lines")
  end,
})
