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

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT

const Bot = () => {
  const [buyBots, setBuyBots] = React.useState([])
  const [toast, addToast] = useState(0)
  const toaster = useRef()
  const state = {
    firsTime: 0
  };

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
    const intervalId = setInterval(getBuyBotList, 2000);
    return () => clearInterval(intervalId);
  });

  const getBuyBotList = async () => {
    try {
      const { data } = await axios.get(
        `${API_ENDPOINT}/trade/upbit/bot/list/buy`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );

      setBuyBots(data)
    } catch (error) {
      console.error(error)
    }
  }

  const deleteBot = async (botId) => {
    try {
      const { data } = await axios.delete(
        `${API_ENDPOINT}/trade/upbit/bot/delete/${botId}`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );
      addToast(notifyToast("봇 성공 삭제."))
    } catch (error) {
      console.error(error)
    }
    getBuyBotList();
  }

  const activeBot = async (botId) => {
    try {
      const { data } = await axios.post(
        `${API_ENDPOINT}/trade/upbit/bot/active/${botId}`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );
      addToast(notifyToast("활성 구매 봇"))
    } catch (error) {
      console.error(error)
    }
    getBuyBotList();
  }

  const stopBot = async (botId) => {
    try {
      const { data } = await axios.post(
        `${API_ENDPOINT}/trade/upbit/bot/stop/${botId}`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }
      );
      addToast(notifyToast("구매 봇 중지"))
    } catch (error) {
      console.error(error)
    }
    getBuyBotList();
  }

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>Buy BOT</strong> <small></small>
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
                      <CTableHeaderCell scope="col">마켓코인</CTableHeaderCell>
                      <CTableHeaderCell scope="col">용량</CTableHeaderCell>
                      <CTableHeaderCell scope="col">주문 유형</CTableHeaderCell>
                      <CTableHeaderCell scope="col">상태</CTableHeaderCell>
                      <CTableHeaderCell scope="col">행동</CTableHeaderCell>
                    </CTableRow>
                  </CTableHead>
                  <CTableBody>
                    {buyBots.map((bot, index) => (
                      <CTableRow key={index}>
                        <CTableHeaderCell scope="row">{index + 1}</CTableHeaderCell>
                        <CTableDataCell>{bot.market}</CTableDataCell>
                        <CTableDataCell>{bot.trade_volume}</CTableDataCell>
                        <CTableDataCell>{bot.ask_bid}</CTableDataCell>
                        <CTableDataCell>{bot.is_expired ? <CBadge color="warning">비활성</CBadge> : <CBadge color="primary">활동적인</CBadge>}</CTableDataCell>
                        <CTableDataCell>
                          {bot.is_expired ? (
                            <button className="btn btn-primary me-1" onClick={() => activeBot(bot.market)}>Active</button>
                          ) : (
                            <button className="btn btn-warning me-1" onClick={() => stopBot(bot.market)}>Stop</button>
                          )}
                          <button className="btn btn-danger me-1" onClick={() => deleteBot(bot.market)}>Delete</button>
                        </CTableDataCell>
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
