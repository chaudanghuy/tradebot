import React, { useRef, useState } from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CFormTextarea,
  CRow,
  CFormCheck,
  CFormSwitch,
  CToast,
  CToastBody,
  CToastClose,
  CToastHeader,
  CToaster,
} from '@coreui/react'
import { DocsExample } from '../../components'
import axios from 'axios'

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT

const Setting = () => {
  const [settingConfig, setSettingConfig] = React.useState({});
  const [toast, addToast] = useState(0)
  const toaster = useRef()

  React.useEffect(() => {
    getSettingConfig();
  }, []);

  const getSettingConfig = async () => {
    const res = await axios.get(`${API_ENDPOINT}/trade/upbit/setting`);
    setSettingConfig(res.data[0]);
  }

  const handleSubmitSetting = async (e) => {
    e.preventDefault()
    const accessKey = document.getElementById('accessKey').value
    const secretKey = document.getElementById('secretKey').value
    const currency = document.getElementById('currency').value
    const time_sleep = document.getElementById('time_sleep').value
    const pumping_rate = document.getElementById('pumping_rate').value
    const data = {
      accessKey,
      secretKey,
      currency,
      time_sleep,
      pumping_rate,
    }

    const response = await axios.post(`${API_ENDPOINT}/trade/upbit/setting/update`, data, {
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

  return (
    <>
      <CRow>
        <CCol xs={12}>
          <CCard className="mb-4">
            <CCardHeader>
              <strong>Setting</strong> <small></small>
            </CCardHeader>
            <CCardBody>
              <p className="text-medium-emphasis small">
                액세스 키와 비밀 키, 기타 설정을 업데이트하세요.
              </p>
              <DocsExample href="components/accordion">
                <CForm onSubmit={handleSubmitSetting}>
                  <CRow className="mb-3">
                    <CFormLabel htmlFor="staticEmail" className="col-sm-2 col-form-label">
                      Upbit Access Key
                    </CFormLabel>
                    <div className="col-sm-10">
                      <CFormInput type="text" id="accessKey" defaultValue={settingConfig.accessKey} />
                    </div>
                  </CRow>
                  <CRow className="mb-3">
                    <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                      Upbit Secret Key
                    </CFormLabel>
                    <div className="col-sm-10">
                      <CFormInput type="text" id="secretKey" defaultValue={settingConfig.secretKey} />
                    </div>
                  </CRow>
                  <CRow className="mb-3">
                    <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                      Currency
                    </CFormLabel>
                    <div className="col-sm-10">
                      <CFormInput type="text" id="currency" defaultValue={settingConfig.currency} placeholder='Trading Currency' />
                    </div>
                  </CRow>
                  <CRow className="mb-3">
                    <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                      Pumping Rate
                    </CFormLabel>
                    <div className="col-sm-10">
                      <CFormInput type="text" id="pumping_rate" defaultValue={settingConfig.pumping_rate} placeholder='Compare volume pumping' />
                    </div>
                  </CRow>
                  <CRow className="mb-3">
                    <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                      Interval Time (ms)
                    </CFormLabel>
                    <div className="col-sm-10">
                      <CFormInput type="text" id="time_sleep" defaultValue={settingConfig.time_sleep} />
                    </div>
                  </CRow>
                  {/* <CRow className="mb-3">
                    <div className="col-sm-10">
                      <CFormCheck id="flexCheckDefault" label="Deactive BOT(s) if expire 1 day" />
                      <CFormCheck id="flexCheckChecked" label="Notify me" defaultChecked />
                    </div>
                  </CRow> */}
                  <div className="col-auto">
                    <CButton type="submit" className="mb-3">
                      Save
                    </CButton>
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

export default Setting
