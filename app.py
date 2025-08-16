from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cab', methods=['GET', 'POST'])
def email_form():
    names = ['Select a Name']
    try:
        with open('employee.txt', 'r', encoding='utf-8') as f:
            names += [line.strip() for line in f if line.strip()]
    except Exception:
        pass
    locations = ['Dhaka', 'Chittagong', 'Sylhet']
    car_types = ['Sedan', 'MPV/Microbus', 'SUV']
    service_types = ['Airport Transfer', '4 Hours Service', '6 Hours Service', '9 Hours Service', '12 Hours Service']
    compliance_docs = [
        'Driving License',
        'Car Tax Token',
        'Car Fitness',
        'Car Registration'
    ]
    reporting_details_default = [
        {'date': '18th August', 'details': 'Cab will report at Dhaka International Airport at 1PM (09 Hours Package)'},
        {'date': '19th August', 'details': 'Cab will report at Westin at 8.00a.m.and will be at disposal with the guest till her drop at Westin. (12 Hours Package (Full Day))'},
        {'date': '20th August', 'details': 'Cab will report at Westin at 8.00a.m.and will be at disposal with the guest till her drop at Westin. (12 Hours Package (Full Day))'},
        {'date': '21st August', 'details': 'Cab will report at Westin at 8.00a.m.and will be at disposal with the guest till her drop at Westin. (12 Hours Package (Full Day))'},
    ]
    if request.method == 'POST':
        date_type = request.form.get('date_type')
        from datetime import datetime
        def format_date(date_str):
            if not date_str:
                return ''
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%b-%Y')
            except Exception:
                return date_str
        reporting_details = []
        date_mode = request.form.get('date_mode')
        reporting_details = []
        dates = []
        if date_mode == 'range':
            from datetime import datetime, timedelta
            service_start = request.form.get('service_start')
            service_end = request.form.get('service_end')
            range_same_service_type = request.form.get('range_same_service_type')
            service_type_range_value = request.form.get('service_type_range_value')
            service_type_start = request.form.get('service_type_start')
            service_type_end = request.form.get('service_type_end')
            date_list = []
            if service_start and service_end:
                start_dt = datetime.strptime(service_start, '%Y-%m-%d')
                end_dt = datetime.strptime(service_end, '%Y-%m-%d')
                delta = (end_dt - start_dt).days
                for i in range(delta + 1):
                    current_dt = start_dt + timedelta(days=i)
                    date_list.append(current_dt)
            elif service_start:
                date_list.append(datetime.strptime(service_start, '%Y-%m-%d'))
            elif service_end:
                date_list.append(datetime.strptime(service_end, '%Y-%m-%d'))
            # For range, display as 'start_date to end_date'
            if date_list:
                if len(date_list) == 1:
                    service_dates = date_list[0].strftime('%d-%b-%Y')
                else:
                    service_dates = f"{date_list[0].strftime('%d-%b-%Y')} to {date_list[-1].strftime('%d-%b-%Y')}"
            else:
                service_dates = ''
            if range_same_service_type:
                note_all = request.form.get('note_all', '')
                for dt in date_list:
                    date_fmt = dt.strftime('%d-%b-%Y')
                    reporting_details.append({'date': date_fmt, 'details': f'{service_type_range_value}: {note_all}' if note_all else service_type_range_value})
            else:
                for dt in date_list:
                    date_fmt = dt.strftime('%d-%b-%Y')
                    note_field = f'note_{dt.strftime("%Y-%m-%d")}'
                    note = request.form.get(note_field, '')
                    field_name = f'service_type_{dt.strftime("%Y-%m-%d")}'
                    service_type = request.form.get(field_name)
                    reporting_details.append({'date': date_fmt, 'details': f'{service_type}: {note}' if note else service_type})
        else:
            # Multiple Dates mode
            dates = []
            reporting_details = []
            same_service_type = request.form.get('same_service_type')
            service_type_all_value = request.form.get('service_type_all_value')
            note_all = request.form.get('note_all', '')
            for i in range(1, 5):
                date_raw = request.form.get(f'service_date{i}')
                if date_raw:
                    dt = datetime.strptime(date_raw, '%Y-%m-%d')
                    date_fmt = dt.strftime('%d-%b-%Y')
                    dates.append(date_fmt)
                    if same_service_type:
                        reporting_details.append({'date': date_fmt, 'details': f'{service_type_all_value}: {note_all}' if note_all else service_type_all_value})
                    else:
                        service_type = request.form.get(f'service_type_{date_raw}')
                        note = request.form.get(f'note_{date_raw}', '')
                        reporting_details.append({'date': date_fmt, 'details': f'{service_type}: {note}' if note else service_type})
            if len(dates) == 1:
                service_dates = dates[0]
            else:
                service_dates = ', '.join(dates)
        data = {
            'name': request.form.get('name'),
            'service_dates': service_dates,
            'service_location': request.form.get('service_location'),
            'pax': request.form.get('pax'),
            'car_type': request.form.get('car_type'),
            'project_code': request.form.get('project_code'),
            'service_type': request.form.get('service_type'),
            'reporting_details': reporting_details,
            'compliance_docs': compliance_docs
        }
        # Validation: If name is 'Select a Name', show error and re-render form
        if data['name'] == 'Select a Name':
            error = 'Please select a valid name.'
            return render_template('form.html', names=names, locations=locations, car_types=car_types, service_types=service_types, error=error)
        return render_template('email_template.html', data=data)
    return render_template('form.html', names=names, locations=locations, car_types=car_types, service_types=service_types)

@app.route('/hotel', methods=['GET', 'POST'])
def hotel_form():
    names = ['Select a Name']
    try:
        with open('employee.txt', 'r', encoding='utf-8') as f:
            names += [line.strip() for line in f if line.strip()]
    except Exception:
        pass
    if request.method == 'POST':
        # Collect all guest sections
        guests = []
        i = 1
        from datetime import datetime
        def format_date(date_str):
            if not date_str:
                return ''
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%b-%Y')
            except Exception:
                return date_str
        while True:
            name = request.form.get(f'name{i}')
            checkin = request.form.get(f'checkin{i}')
            checkout = request.form.get(f'checkout{i}')
            room_type = request.form.get(f'room_type{i}')
            payment_mode = request.form.get(f'payment_mode{i}')
            airport_transfer = request.form.get(f'airport_transfer{i}')
            airport_info = request.form.get(f'airport_info{i}', '')
            if name and name != 'Select a Name':
                if airport_transfer == 'Required':
                    airport_transfer_out = f"Required. {airport_info}" if airport_info else "Required."
                else:
                    airport_transfer_out = airport_transfer
                guest = {
                    'name': name,
                    'checkin': format_date(checkin),
                    'checkout': format_date(checkout),
                    'room_type': room_type,
                    'payment_mode': payment_mode,
                    'airport_transfer': airport_transfer_out
                }
                guests.append(guest)
                i += 1
            else:
                break
        if not guests:
            error = 'Please add at least one valid guest.'
            return render_template('hotel_form.html', names=names, error=error)
        data = {'guests': guests}
        return render_template('hotel_email_template.html', data=data)
    return render_template('hotel_form.html', names=names)

@app.route('/cabtouser')
def cab_to_user_email():
    return render_template('cab_to_user_email_template.html')

@app.route('/hoteltoguest')
def hotel_to_guest_email():
    return render_template('hotel_to_guest_email_template.html')

@app.route('/airtickettouser')
def air_ticket_to_user_email():
    return render_template('air_ticket_to_user_email_template.html')

@app.route('/dhlcourierdone')
def dhl_courier_done_email():
    return render_template('dhl_courier_done_email_template.html')

@app.route('/airticketvendor', methods=['GET', 'POST'])
def air_ticket_vendor_form():
    guests = []
    try:
        with open('guests.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    guests.append({
                        'id': parts[0],
                        'name': parts[1],
                        'email': parts[2],
                        'mobile': parts[3],
                        'project_code': parts[4],
                        'instructions': parts[5]
                    })
    except Exception:
        pass
    if request.method == 'POST':
        guest_id = request.form.get('guest')
        guest = next((g for g in guests if g['id'] == guest_id), None)
        return render_template('air_ticket_request_vendor_email_template.html', guest=guest)
    return render_template('air_ticket_request_vendor_form.html', guests=guests)

if __name__ == '__main__':
    app.run(debug=True)
