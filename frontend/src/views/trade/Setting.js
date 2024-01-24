import React from 'react'
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
} from '@coreui/react'
import { DocsExample } from '../../components'

const Setting = () => {
  return (
    <CRow>
      <CCol xs={12}>
        <CCard className="mb-4">
          <CCardHeader>
            <strong>Setting</strong> <small></small>
          </CCardHeader>
          <CCardBody>
            <p className="text-medium-emphasis small">
              Update your access key and secret key, other settings..
            </p>
            <DocsExample href="components/accordion">
              <CRow className="mb-3">
                <CFormLabel htmlFor="staticEmail" className="col-sm-2 col-form-label">
                  Upbit Access Key
                </CFormLabel>
                <div className="col-sm-10">
                  <CFormInput type="password" id="accessKey" value="123456789" />
                </div>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                  Upbit Secret Key
                </CFormLabel>
                <div className="col-sm-10">
                  <CFormInput type="password" id="secretKey" value="123456789" />
                </div>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                  Profit Rate
                </CFormLabel>
                <div className="col-sm-10">
                  <CFormInput type="text" id="profitRate" value="10%" />
                </div>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel htmlFor="inputPassword" className="col-sm-2 col-form-label">
                  Interval Time (ms)
                </CFormLabel>
                <div className="col-sm-10">
                  <CFormInput type="text" id="intervalTime" value="1000" />
                </div>
              </CRow>
              <CRow className="mb-3">
                <div className="col-sm-10">
                  <CFormCheck id="flexCheckDefault" label="Deactive BOT(s) if expire 1 day" />
                  <CFormCheck id="flexCheckChecked" label="Notify me" defaultChecked />
                </div>
              </CRow>
              <div className="col-auto">
                <CButton type="submit" className="mb-3">
                  Save
                </CButton>
              </div>
            </DocsExample>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default Setting
