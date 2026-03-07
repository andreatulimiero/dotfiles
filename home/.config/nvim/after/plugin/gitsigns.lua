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
