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
    timeout: 1000,
    params: {
      data
    },
    method: 'get'
  })
}

export const ajaxExamGet = (url, data) => {
  return axios.request({
    url: url,
    timeout: 1000,
    method: 'get',
    params: data,
    withCredentials: true
  })
}

export const ajaxPost = (url, params) => {
  const data = JSON.stringify(params)
  return axios.request({
    url: url,
    data: data,
    timeout: 3000,
    method: 'post',
    withCredentials: true
  })
}
