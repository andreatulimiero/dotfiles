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
