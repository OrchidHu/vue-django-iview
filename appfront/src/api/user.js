import axios from '@/libs/api.request'
import config from '@/config'

export const login = ({ userName, password }) => {
  const username = userName
  const data = {
    username,
    password
  }
  return axios.request({
    url: config.loginUrl,
    data,
    method: 'post'
  })
}

export const logout = () => {
  return axios.request({
    url: config.logoutUrl,
    method: 'get',
    withCredentials: true
  })
}

export const ajaxGet = (url, data) => {
  return axios.request({
    url: url,
    params: {
      data
    },
    method: 'get'
  }, 1000)
}
