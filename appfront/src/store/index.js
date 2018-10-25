import Vue from 'vue'
import Vuex from 'vuex'
import { setToken, getToken, setUserName, setSessionId } from '@/libs/util'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userName: '',
    userId: '',
    avatorImgPath: '',
    token: getToken(),
    access: '',
    hasGetInfo: false,
    sessionId: ''
  },
  mutations: {
    setAvator (state, avatorPath) {
      state.avatorImgPath = avatorPath
    },
    setUserId (state, id) {
      state.userId = id
    },
    setUserName (state, name) {
      state.userName = name
      setUserName(name)
    },
    setAccess (state, access) {
      state.access = access
    },
    setToken (state, token) {
      state.token = token
      setToken(token)
    },
    setHasGetInfo (state, status) {
      state.hasGetInfo = status
    },
    setSessionId (state, sessionId){
      state.sessionId = sessionId
      setSessionId(sessionId)
    }
  },
})
