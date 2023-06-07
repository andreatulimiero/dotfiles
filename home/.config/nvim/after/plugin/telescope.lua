local builtin = require('telescope.builtin')
vim.keymap.set('n', '<C-p>', function()
	vim.fn.system('git rev-parse --is-inside-work-tree')
	if vim.v.shell_error == 0 then
		builtin.git_files()
	else
		builtin.find_files()
	end
end)
