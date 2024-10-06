local success, ranger_nvim = pcall(require, "ranger-nvim")
if not success then
  print("Ranger module not found, aborting ranger.lua execution")
  return
end
ranger_nvim.setup({
  enable_cmds = false,
  keybinds = {
    ["ov"] = ranger_nvim.OPEN_MODE.vsplit,
    ["oh"] = ranger_nvim.OPEN_MODE.split,
    ["ot"] = ranger_nvim.OPEN_MODE.tabedit,
    ["or"] = ranger_nvim.OPEN_MODE.rifle,
  },
})
