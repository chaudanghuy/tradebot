import React from 'react'
import { CFooter } from '@coreui/react'

const AppFooter = () => {
  return (
    <CFooter>
      <div>
        <a href="https://localhost" target="_blank" rel="noopener noreferrer">
          Trade App
        </a>
        <span className="ms-1">&copy; 2024.</span>
      </div>
    </CFooter>
  )
}

export default React.memo(AppFooter)
