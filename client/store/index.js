export const state = () => ({
  user: null,
  errorMsg: null
})

export const mutations = {
  login(state, user) {
    state.user = user
  },
  logout(state) {
    state.user = null
  },
  setErrorMsg(state, msg) {
    state.errorMsg = msg
  }
}