import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT

const Private = ({ Component }) => {
  const [message, setMessage] = useState('')
  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      (async () => {
        try {
          const { data } = await axios.get(
            `${API_ENDPOINT}/trade/home`, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              Accept: 'application/json',
            }
          }
          );
          setMessage(data.message)
        } catch (error) {
          console.error(error)
        }
      })()
    };
  }, [])
  // Containers  

  const auth = (localStorage.getItem('access_token') !== null)
  return auth ? <Component /> : <Navigate to="/login" />;
}

export default Private
