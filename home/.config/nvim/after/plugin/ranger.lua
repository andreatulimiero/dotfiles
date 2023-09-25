local ranger_nvim
local success, err = pcall(function ()
  ranger_nvim = require("ranger-nvim")
end)
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
