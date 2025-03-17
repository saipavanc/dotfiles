return {
  {
    "L3MON4D3/LuaSnip",
    version = "2.*",
    config = function()
      local ls = require("luasnip")
      ls.setup({ enable_autosnippets = true })
    end,
  },
}
