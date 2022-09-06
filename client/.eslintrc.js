module.exports = {
  'globals': {
    '$': false,
  },
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    'camelcase': 'off',
    'vue/multi-word-component-names': 'off',
  },
}
