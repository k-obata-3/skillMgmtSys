export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'スキル管理システム',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    'element-ui/lib/theme-chalk/index.css',
    'assets/common.css'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/element-ui',
    {src: '~/plugins/utils.js'},
    {src: '~/plugins/apiService.js'}
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    // eslintは無効にしておく
    // '@nuxtjs/eslint-module'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    'nuxt-fontawesome',
  ],

  fontawesome: {
    imports: [
      {
        set: '@fortawesome/free-brands-svg-icons',
        icons: ['fab']
      },
      {
        set: '@fortawesome/free-solid-svg-icons',
        icons: ['fas']
      },
      {
        set: '@fortawesome/free-regular-svg-icons',
        icons: ['far']
      }
    ]
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    // baseURL: 'http://192.168.0.250:3000/api/',
    baseURL: 'http://127.0.0.1:8000/api/',
    credentials: true,
  },

  // proxy: {
  //   "/api/": {
  //     target: 'http://127.0.0.1:8000',
  //     // pathRewrite: {'^/api/': '/'},
  //   }
  // },

  server: {
    host: '0.0.0.0', // デフォルト: localhost,
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: [/^element-ui/]
  },

  router: {
    // 公開サーバに配置する際は npm run generate を実行
    // base: '/client/',
    extendRoutes(routes, resolve) {
      routes.forEach(route => {
        if (route.name === 'index') {
          route.name = 'ログイン',
          route.meta = {index: 1, hidden: false, select: false, requiresAuth: false, icon: ['fas', 'right-to-bracket']}
        }
        else if (route.name === 'Home') {
          route.path = '/home',
          route.name = 'ホーム',
          route.meta = {index: 2, hidden: false, select: false, requiresAuth: false, icon: ['fa', 'chart-line']}
        }
        else if (route.name === 'ProjectList') {
          route.path = '/projectList',
          route.name = 'プロジェクト一覧',
          route.meta = {index: 3, hidden: true, select: false, requiresAuth: false, icon: ['fas', 'project-diagram']}
        }
        else if (route.name === 'MemberList') {
          route.path = '/memberList',
          route.name = 'メンバー一覧',
          route.meta = {index: 4, hidden: false, select: false, requiresAuth: false, icon: ['fas', 'users']}
        }
        else if (route.name === 'UserSetting') {
          route.path = '/userSetting',
          route.name = '個人設定',
          route.meta = {index: 5, hidden: false, select: false, requiresAuth: false, icon: ['fas', 'user-cog']}
        }
        else if (route.name === 'CareerSetting') {
          route.path = '/careerSetting',
          route.name = '経歴編集',
          route.meta = {index: 6, hidden: false, select: false, requiresAuth: false, icon: ['fas', 'user-edit']}
        }
        else if (route.name === 'ProjectSetting') {
          path: '/projectSetting',
          route.name = 'プロジェクト管理',
          route.meta = {index: 7, hidden: false, select: false, requiresAuth: true, icon: ['fas', 'list-check']}
        }
        else if (route.name === 'MemberSetting') {
          path: '/memberSetting',
          route.name = 'メンバー管理',
          route.meta = {index: 8, hidden: false, select: false, requiresAuth: true, icon: ['fas', 'users-cog']}
        }
        else if (route.name === 'MasterSetting') {
          path: '/masterSetting',
          route.name = 'マスタ管理',
          route.meta = {index: 9, hidden: false, select: false, requiresAuth: true, icon: ['fas', 'cubes']}
        }
      })
      routes.push({
        path: '/logout',
        name: 'ログアウト',
        meta: {index: 9, hidden: false, select: false, requiresAuth: false, icon: ['fas', 'right-from-bracket']}
      })

      routes.sort((a, b) => {
        if (a.meta.index < b.meta.index) return -1;
        if (a.meta.index > b.meta.index) return 1;
        return 0;
      });
    },
  },
}
