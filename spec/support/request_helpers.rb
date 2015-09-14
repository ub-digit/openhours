module Requests
  module JsonHelpers
    def json
      unless @last_response_body === response.body
        @json = nil
      end
      @last_response_body = response.body
      @json ||= JSON.parse(response.body)
    end

    def setup_locations
      ActiveRecord::Base.connection.execute("DELETE FROM lokal")
      ActiveRecord::Base.connection.execute("DELETE FROM lokal_sort")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal VALUES (1, 'Plats 4', 'Location 1')")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal VALUES (2, 'Plats 3', 'Location 2')")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal VALUES (3, 'Plats 2', 'Location 3')")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal VALUES (4, 'Plats 1', 'Location 4')")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal_sort VALUES (1, 0)")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal_sort VALUES (2, 0)")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal_sort VALUES (3, 1)")
      ActiveRecord::Base.connection.execute("INSERT INTO lokal_sort (id) VALUES (4)")
    end

    def setup_openhours
      ActiveRecord::Base.connection.execute("DELETE FROM openhours")
      weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
      stamps1 = {
        1 => [[8.30, 16.30]]*5+[[10.00, 10.00], [10.00, 10.00]],
        2 => [[8.30, 18.00]]*4+[[ 8.30, 13.00], [10.00, 16.00], [10.00, 16.00]],
        3 => [[9.00, 18.30]]*5+[[10.00, 10.00], [10.00, 10.00]],
      }
      stamps2 = {
        1 => [[8.30, 13.30]]*5+[[10.00, 10.00], [10.00, 10.00]],
        2 => [[9.30, 15.00]]*5+[[10.00, 16.00], [10.00, 10.00]],
        3 => [[10.00, 16.00]]*5+[[10.00, 10.00], [10.00, 10.00]],
      }
      exceptions = [
        [1, '2014-06-01', 9.00, 9.00],
        [1, '2014-06-02', 9.00, 9.00],
        [1, '2014-07-01', 9.00, 11.00],
        [1, '2014-10-01', 9.00, 9.00],
        [1, '2014-10-02', 9.00, 9.00],
        [1, '2014-11-01', 11.00, 13.00],
      ]
      [1, 2, 3].each do |location|
        weekdays.each.with_index do |day,i|
          Openhour.create(lokal_id: location, day: day,
                          open: stamps1[location][i].first,
                          close: stamps1[location][i].last,
                          prioritet: 2,
                          from_dag: '2014-01-01') 
          Openhour.create(lokal_id: location, day: day,
                          open: stamps2[location][i].first,
                          close: stamps2[location][i].last,
                          prioritet: 2,
                          from_dag: '2014-08-01')
        end
      end
      exceptions.each do |exception|
        Openhour.create(lokal_id: exception[0],
                        day: exception[1],
                        open: exception[2],
                        close: exception[3],
                        prioritet: 1)
      end
    end
  end
end
