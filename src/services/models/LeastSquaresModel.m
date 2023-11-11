datasource = "jdbc:postgresql://localhost:5432/hrr-power-db";
username = "postgres";
password = "admin";

conn = postgresql(username, password, 'Server', 'localhost', 'DatabaseName',"hrr-power-db", 'PortNumber', 5432);

% % Extracting data for a specific activity
activityId = 8752058834
testData = getTestData(conn, activityId)

function testData = getTestData(conn, aId)
        sqlquery = "SELECT activity_id, heartrate, ""Power (in watts)"" " + ...
            "FROM ""athletic-data"" " + ...
            "WHERE activity_id ='" + aId + "'";
        %data = fetch(conn,sqlquery);
        %data = fetch(conn,sqlquery,"DataReturnFormat','cell')
        opts = databaseImportOptions(conn,sqlquery)
        vars = opts.SelectedVariableNames;
        opts = setoptions(opts,{'heartrate','Power (in watts)'}, ...
        'Type','cellarray');
        % vars = opts.SelectedVariableNames;
        % varOpts = getoptions(opts,vars) 
        % Import data using SQLImportOptions
  %       disp([opts.VariableNames' opts.VariableTypes'])
 %       vars = opts.SelectedVariableNames;
  %      varOpts = getoptions(opts,vars)
         data = fetch(conn,sqlquery, opts);

        testData = data
end
% 
% hr0_ivp = 75;
% hrt_ivp = 55;
% K_ivp = 0.05;
% tau_ivp = 2;
% pseries_simulated = zeros(3600, 1);
% 
% t = 0;
% p0 = 100 + (30 * t / 180);
% 
% for t = 1:3600
%     pseries_simulated(t) = 100 + (30 * floor(t / 180));
% end
% 
% hr_list_simulated = zeros(3599, 1);
% 
% hr_list_simulated(1) = (hrt_ivp + K_ivp * p0) + (exp(-1 / tau_ivp)) * (hr0_ivp - hrt_ivp - K_ivp * p0);
% 
% for i = 2:3599
%     hr_list_simulated(i) = (hrt_ivp + K_ivp * pseries_simulated(i-1)) + (exp(-1 / tau_ivp)) * (hr_list_simulated(i-1) - hrt_ivp - K_ivp * pseries_simulated(i-1));
% end
% 
% hr_list_all = [hr0_ivp; hr_list_simulated];
% C_ = -hr_list_simulated;
% 
% % Calculate hr_derivative_ivp_test
% hr_derivative_ivp_test = zeros(3599, 1);
% for i = 1:3599
%     hr_derivative_ivp_test(i) = (hrt_ivp + K_ivp * pseries_simulated(i) - hr_list_simulated(i)) / tau_ivp;
% end
% 
% % Create matrix A_ivp
% A_ivp = [hr_derivative_ivp_test, pseries_simulated(1:3599), ones(3599, 1)];
% 
% % Solve for solution_ivp_test
% solution_ivp_test = (A_ivp' * A_ivp) \ (A_ivp' * C_);
% ivp_results = struct('tau_lsm_ivp', solution_ivp_test(1), 'k_lsm_ivp', -solution_ivp_test(2), 'hreq_lsm_ivp', -solution_ivp_test(3));
% 
% % Calculate hr_derivative_basic_test
% hr_derivative_basic_test = diff(hr_list_all);
% A_basic = [hr_derivative_basic_test, pseries_simulated(1:3599), ones(3599, 1)];
% 
% % Solve for solution_basic_test
% solution_basic_test = (A_basic' * A_basic) \ (A_basic' * C_);
% basic_results = struct('tau_lsm_basic', solution_basic_test(1), 'k_lsm_basic', -solution_basic_test(2), 'hreq_lsm_basic', -solution_basic_test(3));
% 
% % Calculate hr_derivative_glla
% hr_derivative_glla = calculate_glla(hr_list_all, 1:3600, 2, 1);
% hr_derivative_glla = hr_derivative_glla(~isnan(hr_derivative_glla));
% A_s_q1 = [hr_derivative_glla, pseries_simulated(1:3599), ones(length(hr_derivative_glla), 1)];
% 
% % Solve for solution_sq1_test
% solution_sq1_test = (A_s_q1' * A_s_q1) \ (A_s_q1' * C_);
% s_g1_results = struct('tau_lsm_sg', solution_sq1_test(1), 'k_lsm_sg', -solution_sq1_test(2), 'hreq_lsm_sg', -solution_sq1_test(3));
% 
% % Calculate hr_derivative_savitzy_golay
% hr_derivative_savitzy_golay = savgolay(hr_list_all, 3599, 4, 1);
% A_s_q2 = [hr_derivative_savitzy_golay, pseries_simulated(1:3599), ones(length(hr_derivative_savitzy_golay), 1)];
% 
% % Solve for solution_sq2_test
% solution_sq2_test = (A_s_q2' * A_s_q2) \ (A_s_q2' * C_);
% s_g2_results = struct('tau_lsm_sg', solution_sq2_test(1), 'k_lsm_sg', -solution_sq2_test(2), 'hreq_lsm_sg', -solution_sq2_test(3));
% 
% % Display results
% disp(ivp_results);
% disp(basic_results);
% disp(s_g1_results);
% disp(s_g2_results);
% 
% % Initialize additional parameters for the MATLAB code
% HR_0 = hr_list_all(1);
% exp_hr_new = zeros(length(pseries_simulated), 1);
% time_vector = 1:3600;
% options = struct('digits', 15);
% est_hr = zeros(3599, 1);
% 
% % Set the parameter values
% tau_test = s_g2_results.tau_lsm_sg;
% k_test = -s_g2_results.k_lsm_sg;
% hr_eq_test = -s_g2_results.hreq_lsm_sg;
% 
% % Initialize the first value of est_hr
% est_hr(1) = predict_hr(p0, 1, hr0_ivp);
% 
% % Calculate estimated HR values
% for i = 2:3599
%     est_hr(i) = predict_hr(pseries_simulated(i - 1), 1, est_hr(i - 1));
% end
% 
% % Calculate RMSE
% rmse_test = sqrt(mean((est_hr - hr_list_simulated).^2));
% disp(rmse_test);
% 
% % Define the predict_hr function
% function hr_t = predict_hr(pow, t, hr)
%     hr_t = (hr_eq_test + k_test * pow) + exp(-t / tau_test) * (hr - hr_eq_test - k_test * pow);
% end

