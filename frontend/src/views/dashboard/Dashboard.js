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
import TradeCoin from '../trade/TradeCoin'
import axios from 'axios'

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT

const Trade = () => {

  const [coins, setCoins] = React.useState([])
  const [selectedCoin, setSelectedCoin] = React.useState('')
  const [currentPrice, setCurrentPrice] = React.useState('')
  const [candle, setCandle] = React.useState([])
  const [candlePriceList, setCandlePriceList] = React.useState('')
  const [tradeBotTotal, setTradeBotTotal] = React.useState(0)
  const [isDetecingPump, setIsDetecingPump] = React.useState(false)
  const [balance, setBalance] = React.useState(0)
  const state = {
    button: 1
  };
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
      axios.get(`${API_ENDPOINT}/trade/upbit/coin`, {
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

      getWallet();
    }

    if (selectedCoin) {
      getSelectedCoin();
    }
  });

  const getWallet = async () => {
    try {
      axios.get(`${API_ENDPOINT}/trade/upbit/account`, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          Accept: 'application/json',
        }
      }).then(res => {
        setBalance(res.data.balances[0].balance)
        setTradeBotTotal(res.data.total)
      }).catch(err => {
        console.log(err)
      });
    } catch (error) {
      console.log(error)
    }
  }

  const getSelectedCoin = async () => {
    try {
      axios.get(`${API_ENDPOINT}/trade/upbit/market/coin?market=${selectedCoin}`, {
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
        setIsDetecingPump(res.data.is_detecting_pump)

      }).catch(err => {
        console.log(err)
      });
    } catch (error) {

    }
  }

  const handleSelectedCoin = (e) => {
    setSelectedCoin(e.target.value)
  }

  const handleSubmitBot = async (e) => {
    e.preventDefault()
    const saleOrBuy = (state.button == 1) ? 'buy' : 'sale';
    const market = document.getElementById('market_bot').value
    const ask_bid = document.getElementById('ask_bid_bot').value
    const trade_price = 999
    const volume = document.getElementById('volume_bot').value
    const data = {
      market,
      ask_bid,
      trade_price,
      volume
    }

    const response = await axios.post(`${API_ENDPOINT}/trade/upbit/bot/${saleOrBuy}`, data, {
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
                    <option value={coin.market}>{coin.korean_name}</option>
                  ))}
                </CFormSelect>
              </DocsExample>
            </CCardBody>
          </CCard>
        </CCol>
        <TradeCoin price={currentPrice} candlePriceList={candlePriceList} tradeBotTotal={tradeBotTotal} isDetecingPump={isDetecingPump} balance={balance} />
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
              <strong>New BOT</strong> <small>코인 자동매매 </small>
            </CCardHeader>
            <CCardBody>
              <DocsExample href="forms/form-control">
                <CForm onSubmit={handleSubmitBot}>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlInput1">Coin</CFormLabel>
                    <CFormSelect aria-label="Default select example" id='market_bot'>
                      {coins.map((coin) => (
                        <option value={coin.market}>{coin.market}</option>
                      ))}
                    </CFormSelect>
                  </div>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlTextarea1">Order Price</CFormLabel>
                    <CFormSelect aria-label="Default select example" id='ask_bid_bot'>
                      <option value="limit">Limit</option>
                      <option value="price">Price</option>
                      <option value="market">Market</option>
                    </CFormSelect>
                  </div>
                  <div className="mb-3">
                    <CFormLabel htmlFor="exampleFormControlInput1">Volume</CFormLabel>
                    <CFormInput
                      type="text"
                      id="volume_bot"
                      placeholder="Total Volume"
                    />
                  </div>
                  <div className='mb-3'>
                    <button type="submit" onClick={() => (state.button = 1)} class="btn btn-primary me-1">BUY</button>
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
