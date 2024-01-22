import React, { useRef, useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CTable,
  CTableBody,
  CTableCaption,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CBadge,
  CToast,
  CToastBody,
  CToastClose,
  CToastHeader,
  CToaster,
} from '@coreui/react'
import { DocsExample } from '../../components'
import axios from 'axios'

const Bot = () => {
  const [bots, setBots] = React.useState([])
  const [toast, addToast] = useState(0)
  const toaster = useRef()

  const notifyToast = (message) => {
    return <CToast title="Notification">
      <CToastHeader closeButton>
        <svg
          className="rounded me-2"
          width="20"
          height="20"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid slice"
          focusable="false"
          role="img"
        >
          <rect width="100%" height="100%" fill="#007aff"></rect>
        </svg>
        <strong className="me-auto">Notification</strong>
        <small></small>
      </CToastHeader>
      <CToastBody>{message}</CToastBody>
    </CToast>
  }

  React.useEffect(() => {
    const intervalId = setInterval(getBotList, 5000);
    const intervalId2 = setInterval(getLogList, 10000);
    return () => clearInterval(intervalId);
    return () => clearInterval(intervalId2);
  });

  const getBotList = async () => {
    try {
      const { data } = await axios.get(
        'http://127.0.0.1:8000/trade/upbit/bot/list', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );

      setBots(data)
    } catch (error) {
      console.error(error)
    }
  }

  const getLogList = async () => {
    try {
      const { data } = await axios.get(
        'http://127.0.0.1:8000/trade/upbit/bot/log', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );

      // Loop through array and call toast to notify message
      data.forEach(log => {
        addToast(notifyToast(log.message))
      });
    } catch (error) {
      console.error(error)
    }
  }

  const processBotList = async () => {
    try {
      const { data } = await axios.get(
        'http://127.0.0.1:8000/trade/upbit/bot/process', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );
    } catch (error) {
      console.error(error)
    }
  }

  const deleteBot = async (botId) => {
    try {
      const { data } = await axios.delete(
        `http://127.0.0.1:8000/trade/upbit/bot/delete/${botId}`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );
      addToast(notifyToast("Delete Bot Success."))
    } catch (error) {
      console.error(error)
    }
    getBotList();
  }

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>BOT Commands</strong> <small></small>
            </CCardHeader>
            <CCardBody>
              <p className="text-medium-emphasis small">
                반복문 시작
              </p>
              <DocsExample href="components/table#hoverable-rows">
                <CTable hover>
                  <CTableHead>
                    <CTableRow>
                      <CTableHeaderCell scope="col">#</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Market</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Price</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Volume</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Ask Order</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Status</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Action</CTableHeaderCell>
                    </CTableRow>
                  </CTableHead>
                  <CTableBody>
                    {bots.map((bot, index) => (
                      <CTableRow key={index}>
                        <CTableHeaderCell scope="row">{index + 1}</CTableHeaderCell>
                        <CTableDataCell>{bot.market}</CTableDataCell>
                        <CTableDataCell>{bot.trade_price}</CTableDataCell>
                        <CTableDataCell>{bot.trade_volume}</CTableDataCell>
                        <CTableDataCell>{bot.ask_bid}</CTableDataCell>
                        <CTableDataCell>{bot.is_completed ? <CBadge color="success">Success</CBadge> : <CBadge color="primary">Running</CBadge>}</CTableDataCell>
                        <CTableDataCell><button className="btn btn-danger" onClick={() => deleteBot(bot.market)}>Delete</button></CTableDataCell>
                      </CTableRow>
                    ))}
                  </CTableBody>
                </CTable>
              </DocsExample>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
      <CToaster ref={toaster} push={toast} placement="top-end" />
    </>
  )
}

export default Bot
