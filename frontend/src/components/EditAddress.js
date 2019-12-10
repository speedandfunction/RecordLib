import React from "react";
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField'


function EditAddress(props) {
    const { header, address, modifier } = props;
    const addressStyle = { gridColumn: "1 / 3",  margin: '25px 0', width: '425px' };

    const getPropertyModifier = key => {
        return event => modifier(key, event.target.value);
    }

    return (
        <div className="editAddress" style={addressStyle}>
            <div>{header}</div>
            <div className="editLine">
                <TextField 
                    label="Address line one"
                    type="text" size="60" value={address.line_one} 
                    onChange={getPropertyModifier('address.line_one')}/>
            </div>
            <div className="editLine">
                 <TextField type="text" size="60" 
                    label="Address line two"
                    value={address.city_state_zip} onChange={getPropertyModifier('address.city_state_zip')}/>
            </div>
        </div>
    );
}

EditAddress.propTypes = {
    header: PropTypes.string,
    address: PropTypes.shape({
        line_one: PropTypes.string,
        city_state_zip: PropTypes.string
    }),
    modifier: PropTypes.func
}

export default EditAddress;