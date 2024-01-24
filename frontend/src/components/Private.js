import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'

const Private = ({ Component }) => {
  const [message, setMessage] = useState('')
  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      (async () => {
        try {
          const { data } = await axios.get(
            'http://51.79.49.245/trade/home', {
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
