vim.g.opencode_opts = { }
vim.keymap.set("n", "<C-s>", function()
  return require("opencode").operator("@file ")
end, { expr = true, desc = "Send file to opencode" })
vim.keymap.set({ "n", "x" }, "<C-s>", function()
  return require("opencode").operator("@this ")
end, { expr = true, desc = "Add selection to opencode" })
