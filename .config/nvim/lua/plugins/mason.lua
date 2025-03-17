return {
  "williamboman/mason.nvim",
  dependencies = {
    "williamboman/mason-lspconfig.nvim",
  },
  config = function()
    require("mason").setup()
    require("mason-lspconfig").setup({
      inlay_hints = {
        enabled = true,
        exclude = { "tex" }, -- filetypes for which you don't want to enable inlay hints
      },
    })
  end,
}
