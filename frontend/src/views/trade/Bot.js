import React from 'react'
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
} from '@coreui/react'
import { DocsExample } from '../../components'
import axios from 'axios'

const Bot = () => {
  const [bots, setBots] = React.useState([])

  React.useEffect(() => {
    getBotList()
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

  return (
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
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {bots.map((bot) => (
                    <CTableRow>
                      <CTableHeaderCell scope="row">{bot.timestamp}</CTableHeaderCell>
                      <CTableDataCell>{bot.market}</CTableDataCell>
                      <CTableDataCell>{bot.trade_price}</CTableDataCell>
                      <CTableDataCell>{bot.trade_volume}</CTableDataCell>
                      <CTableDataCell>{bot.ask_bid}</CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
            </DocsExample>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default Bot
