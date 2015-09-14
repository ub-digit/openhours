# -*- coding: utf-8 -*-
require 'rails_helper'

RSpec.describe OpenhoursController, :type => :controller do
  before :each do
    setup_locations
    setup_openhours
  end
  describe "get single day for single location" do
    it "should return timestamps for one location" do
      get :index, location_id: 1, date: '2014-05-01' # Thursday
      expect(json).to have_key('openhour')
      expect(json['openhour']['location']['sv']).to eq('Plats 4')
      expect(json['openhour']['location']['en']).to eq('Location 1')
      expect(json['openhour']['date']).to eq('2014-05-01')
      expect(json['openhour']['weekday']['sv']).to eq('Torsdag')
      expect(json['openhour']['weekday']['en']).to eq('Thursday')
      expect(json['openhour']['open']).to eq("08:30")
      expect(json['openhour']['close']).to eq("16:30")
      expect(json['openhour']['string']['sv']).to eq("08:30 - 16:30")
      expect(json['openhour']['string']['en']).to eq("08:30 - 16:30")
      expect(json['openhour']['is_open']).to be_truthy
      expect(json['openhour']['is_exception']).to be_falsey
      expect(json['openhour']['timestamps']['open']).to eq(Time.parse('2014-05-01 08:30').iso8601(3))
      expect(json['openhour']['timestamps']['close']).to eq(Time.parse('2014-05-01 16:30').iso8601(3))
    end

    it "should return timestamps for one location at later date" do
      get :index, location_id: 2, date: '2014-12-06' # Saturday
      expect(json).to have_key('openhour')
      expect(json['openhour']['location']['sv']).to eq('Plats 3')
      expect(json['openhour']['location']['en']).to eq('Location 2')
      expect(json['openhour']['date']).to eq('2014-12-06')
      expect(json['openhour']['weekday']['sv']).to eq('Lördag')
      expect(json['openhour']['weekday']['en']).to eq('Saturday')
      expect(json['openhour']['open']).to eq("10:00")
      expect(json['openhour']['close']).to eq("16:00")
      expect(json['openhour']['string']['sv']).to eq("10:00 - 16:00")
      expect(json['openhour']['string']['en']).to eq("10:00 - 16:00")
      expect(json['openhour']['is_open']).to be_truthy
      expect(json['openhour']['is_exception']).to be_falsey
      expect(json['openhour']['timestamps']['open']).to eq(Time.parse('2014-12-06 10:00').iso8601(3))
      expect(json['openhour']['timestamps']['close']).to eq(Time.parse('2014-12-06 16:00').iso8601(3))
    end

    it "should return timestamps for one location with exception" do
      get :index, location_id: 1, date: '2014-07-01'
      expect(json).to have_key('openhour')
      expect(json['openhour']['location']['sv']).to eq('Plats 4')
      expect(json['openhour']['location']['en']).to eq('Location 1')
      expect(json['openhour']['date']).to eq('2014-07-01')
      expect(json['openhour']['weekday']['sv']).to eq('Tisdag')
      expect(json['openhour']['weekday']['en']).to eq('Tuesday')
      expect(json['openhour']['open']).to eq("09:00")
      expect(json['openhour']['close']).to eq("11:00")
      expect(json['openhour']['string']['sv']).to eq("09:00 - 11:00")
      expect(json['openhour']['string']['en']).to eq("09:00 - 11:00")
      expect(json['openhour']['is_open']).to be_truthy
      expect(json['openhour']['is_exception']).to be_truthy
      expect(json['openhour']['timestamps']['open']).to eq(Time.parse('2014-07-01 09:00').iso8601(3))
      expect(json['openhour']['timestamps']['close']).to eq(Time.parse('2014-07-01 11:00').iso8601(3))
    end

    it "should return timestamps for one location which is closed" do
      get :index, location_id: 1, date: '2014-05-03' # Saturday
      expect(json).to have_key('openhour')
      expect(json['openhour']['location']['sv']).to eq('Plats 4')
      expect(json['openhour']['location']['en']).to eq('Location 1')
      expect(json['openhour']['date']).to eq('2014-05-03')
      expect(json['openhour']['weekday']['sv']).to eq('Lördag')
      expect(json['openhour']['weekday']['en']).to eq('Saturday')
      expect(json['openhour']['string']['sv']).to eq("Stängt")
      expect(json['openhour']['string']['en']).to eq("Closed")
      expect(json['openhour']['is_open']).to be_falsey
      expect(json['openhour']['is_exception']).to be_falsey
    end

    it "should return timestamps for one location which is closed with exception" do
      get :index, location_id: 1, date: '2014-10-02'
      expect(json).to have_key('openhour')
      expect(json['openhour']['location']['sv']).to eq('Plats 4')
      expect(json['openhour']['location']['en']).to eq('Location 1')
      expect(json['openhour']['date']).to eq('2014-10-02')
      expect(json['openhour']['weekday']['sv']).to eq('Torsdag')
      expect(json['openhour']['weekday']['en']).to eq('Thursday')
      expect(json['openhour']['string']['sv']).to eq("Stängt")
      expect(json['openhour']['string']['en']).to eq("Closed")
      expect(json['openhour']['is_open']).to be_falsey
      expect(json['openhour']['is_exception']).to be_truthy
    end
  end

  describe "get sequence of days using day count" do
    it "should return list of timestamps for one location" do
      get :index, location_id: 1, start_date: '2014-05-01', days: 7
      expect(json).to have_key('openhours')
      expect(json['openhours']).to be_kind_of(Array)
      expect(json['openhours'].count).to eq(7)
      expect(json['openhours'][0]['date']).to eq('2014-05-01')
    end
  end
end
