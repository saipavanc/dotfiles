return {
  "lervag/vimtex",
  lazy = false,
  config = function()
    vim.g.tex_flavor = "latex"
    vim.g.vimtex_view_method = "zathura"
    -- vim.g.vimtex_quickfix_mode = 0
    vim.g.vimtex_compiler_method = "tectonic"
    vim.g.vimtex_compiler_tectonic = {
      options = {
        "--synctex",
        "--keep-logs",
        "--keep-intermediates",
      },
    }
  end,
}
