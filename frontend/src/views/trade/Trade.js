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
  CFormSelect,
  CForm,
  CFormLabel,
  CFormInput,
  CFormTextarea,
  CToast,
  CToastBody,
  CToastClose,
  CToastHeader,
  CToaster,
} from '@coreui/react'
import { DocsExample } from '../../components'
import TradeCoin from './TradeCoin'
import axios from 'axios'

const Trade = () => {

  const [coins, setCoins] = React.useState([])
  const [selectedCoin, setSelectedCoin] = React.useState('')
  const [currentPrice, setCurrentPrice] = React.useState('')
  const [candle, setCandle] = React.useState([])
  const [candlePriceList, setCandlePriceList] = React.useState('')
  const [toast, addToast] = useState(0)
  const toaster = useRef()

  const notifyToast = (
    <CToast title="Notification">
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
      <CToastBody>Add Bot Success.</CToastBody>
    </CToast>
  )

  React.useEffect(() => {
    if (coins.length <= 0) {
      axios.get('http://127.0.0.1:8000/trade/upbit/market', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }).then(res => {
        setCoins(res.data)
      }).catch(err => {
        console.log(err)
      });
    }

    if (selectedCoin) {
      axios.get(`http://127.0.0.1:8000/trade/upbit/market/coin?market=${selectedCoin}`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }).then(res => {
        setCurrentPrice(res.data.price)
        setCandle(res.data.candle)
        setCandlePriceList(res.data.formatted_candle_price.map((price) => {
          return price
        }).join(','))
      }).catch(err => {
        console.log(err)
      });
    }
  });

  const handleSelectedCoin = (e) => {
    setSelectedCoin(e.target.value)
  }

  const handleSubmitBot = async (e) => {
    e.preventDefault()
    const market = document.getElementById('market_bot').value
    const ask_bid = document.getElementById('ask_bid_bot').value
    const trade_price = document.getElementById('trade_price_bot').value
    const volume = document.getElementById('volume_bot').value
    const data = {
      market,
      ask_bid,
      trade_price,
      volume
    }

    const response = await axios.post('http://127.0.0.1:8000/trade/upbit/bot', data, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        Accept: 'application/json',
      }
    }).then(res => {
      addToast(notifyToast)
    }).catch(err => {
      console.log(err)
    })
  }

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>Find coin</strong> <small></small>
            </CCardHeader>
            <CCardBody>
              <DocsExample href="forms/select">
                <CFormSelect aria-label="Default select example" onChange={handleSelectedCoin}>
                  <option>현재가</option>
                  {coins.map((coin) => (
                    <option value={coin.market}>{coin.english_name}</option>
                  ))}
                </CFormSelect>
              </DocsExample>
            </CCardBody>
          </CCard>
        </CCol>
        <TradeCoin price={currentPrice} candlePriceList={candlePriceList} />
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>Orders</strong> <small></small>
            </CCardHeader>
            <CCardBody>
              <p className="text-medium-emphasis small">
                # 1분봉 (최대 200개 요청가능)
              </p>
              <DocsExample href="components/table#hoverable-rows">
                <CTable color="dark" hover>
                  <CTableHead>
                    <CTableRow>
                      <CTableHeaderCell scope="col">#</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Open</CTableHeaderCell>
                      <CTableHeaderCell scope="col">High</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Low</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Close</CTableHeaderCell>
                      <CTableHeaderCell scope="col">Volume</CTableHeaderCell>
                    </CTableRow>
                  </CTableHead>
                  <CTableBody>
                    {candle.map((order) => (
                      <CTableRow>
                        <CTableHeaderCell scope="row">{order.timestamp}</CTableHeaderCell>
                        <CTableDataCell>{order.open}</CTableDataCell>
                        <CTableDataCell>{order.high}</CTableDataCell>
                        <CTableDataCell>{order.low}</CTableDataCell>
                        <CTableDataCell>{order.close}</CTableDataCell>
                        <CTableDataCell>{order.volume}</CTableDataCell>
                      </CTableRow>
                    ))}
                  </CTableBody>
                </CTable>
              </DocsExample>
            </CCardBody>
          </CCard>
        </CCol>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>Create BOT</strong> <small>코인 자동매매 </small>
            </CCardHeader>
            <CCardBody>
              <DocsExample href="forms/form-control">
                <CForm onSubmit={handleSubmitBot}>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlInput1">Coin</CFormLabel>
                    <CFormSelect aria-label="Default select example" id='market_bot'>
                      <option>현재가</option>
                      {coins.map((coin) => (
                        <option value={coin.market}>{coin.english_name}</option>
                      ))}
                    </CFormSelect>
                  </div>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlTextarea1">Order Price</CFormLabel>
                    <CFormSelect aria-label="Default select example" id='ask_bid_bot'>
                      <option>주문 유형 (필수)</option>
                      <option value="limit">Limit</option>
                      <option value="price">Price</option>
                      <option value="market">Market</option>
                    </CFormSelect>
                  </div>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlInput1">Fix Order Price (KRW)</CFormLabel>
                    <CFormInput
                      type="number"
                      id="trade_price_bot"
                      placeholder="Fixed Price"
                    />
                  </div>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlInput1">Volume</CFormLabel>
                    <CFormInput
                      type="number"
                      id="volume_bot"
                      placeholder="Total Volume"
                    />
                  </div>
                  <div className='mb-3'>
                    <button type="submit" class="btn btn-primary">CREATE</button>
                  </div>
                </CForm>
              </DocsExample>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
      <CToaster ref={toaster} push={toast} placement="top-end" />
    </>
  )
}

export default Trade
