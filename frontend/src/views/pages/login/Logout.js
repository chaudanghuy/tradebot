import { useEffect, useState } from "react";
import axios from "axios";

export const Logout = () => {
  useEffect(() => {
    (async () => {
      try {
        const { data } = await axios.post(
          'http://127.0.0.1:8000/trade/logout', {
          refresh_token: localStorage.getItem('refresh_token')
        }, {
          headers: {
            'Content-Type': 'application/json',
          }
        },
          {
            withCredentials: true
          }
        );
        localStorage.clear();
        axios.defaults.headers.common['Authorization'] = null;
        window.location.href = '/login';
      } catch (error) {
        console.error(error)
      }
    })();
  }, []);

  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}