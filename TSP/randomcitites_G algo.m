function varargout = randomcities_G algo(varargin)
    
    defaultConfig.xy            =50*rand(100,2);  % 100 cities
    defaultConfig.dmat          = [];
    defaultConfig.popsize       =150;
    defaultConfig.numIter       =1e4;
    defaultConfig.showprog      =true;
    defaultConfig.showResult    =true;
    defaultConfig.showWaitbar   =true;
    
    if ~nargin
        userConfig = struct();
    elseif isstruct(varargin(1));
        userConfig = varargin(1);
    else
        try
            userConfig=struct(varargin{:});
        catch 
            error('error');
            
        end
    end
    %override default config. with user inputs
    configStruct = get_config(defaultConfig,userConfig);
    
    %extract config.
    xy = configStruct.xy;
    dmat = configStruct.dmat;
    popsize = configStruct.popsize;
    numIter = configStruct.numIter;
    showprog =configStruct.showprog;
    showResult = configStruct.showResult;
    showWaitbar = configStruct.showWaitbar;
    
    if isempty(dmat)
        npoints = size(xy,1);
        a=meshgrid(1:npoints);
        dmat = reshape(sqrt(sum((xy(a,:)-xy(a',:)).^2,2)),npoints,npoints);
    end
    
    [N,dims]=size(xy);
    [nr,nc]=size(dmat);
    if N ~= nr || N~=nc
        error('invalid');
    end
    n= N;
    
    popsize = 4*ceil(popsize/4);
    numIter = max(1,round(real(numIter(1))));
    showprog = logical(showprog(1));
    showResult=logical(showResult(1));
    showWaitbar=logical(showWaitbar(1));
    
    
    %intial population
    pop = zeros(popsize,n);
    pop(1,:) = (1:n);
    for k=2:popsize
        pop(k,:)=randperm(n);
    end
        
    %ga
    globalMin = Inf;
    totalDist = zeros(1,popsize);
    disthistroy=zeros(1,numIter);
    temppop=zeros(4,n);
    newpop = zeros(popsize,n);
    
    if showprog
      
        hAx=gca;
    end
    if showWaitbar
     
    end
    
    for iter = 1:numIter
        %total dist.
        for p = 1:popsize
            d = dmat(pop(p,n),pop(p,1)); %closed path
            for k=2:n
                d = d+dmat(pop(p,k-1),pop(p,k));
            end
            totalDist(p)=d;
        end
            %best path population
            [minDist,index] =min(totalDist);
            disthistroy(iter)=minDist;
            if minDist<globalMin
                globalMin=minDist;
                optroute = pop(index,:);
                if showprog
                    rte=optroute([1:n 1]);
                    if dims>2,plot3(hAx,xy(rte,1),xy(rte,2),xy(rte,3),'MarkerEdgeColor',"r");
                    else plot(hAx,xy(rte,1),xy(rte,2),'m.-');end
                    title(hAx,sprintf('total distance=%1.4f,no of iteration=%d',minDist,iter));
                    drawnow;
                end
            end
    %ga algo
            randomorder = randperm(popsize);
            for p = 4:4:popsize
                rtes=pop(randomorder(p-3:p),:);
                dists=totalDist(randomorder(p-3:p));
                [ignore,idx]=min(dists);
                bestof4route=rtes(idx,:);
                routeInsertionpoints=sort(ceil(n*rand(1,2)));
                I=routeInsertionpoints(1);
                J=routeInsertionpoints(2);
                for k=1:4 %mute the best to get three new routes
                    temppop(k,:)=bestof4route;
                    switch k
                        case 2 %flip
                            tempop(k,I:J)=temppop(k,J:-1:I);
                        case 3 %swap
                            temppop(k,[I,J])=temppop(k,[J I]);
                        case 4 %slide
                            tempop(k,I:J)=temppop(k,[I+1:J I]);
                        otherwise           
                    end
                end
                newpop(p-3:p,:)=temppop;
            end
            pop=newpop;
            if showWaitbar && ~mod(iter,ceil(numIter/1000))
               % waitbar(iter/numIter,hwait);
            end
    end
            if showWaitbar
              %  close(hwait);
            end
                if showResult
                    figure('Name','TSP_GA | results','Numbertitle','off');
                    
                    pclr = ~get(0,'DefaultAxesColor');
                    if dims > 2,plot3(xy(:,1),xy(:,2),xy(:,3),'.','Color',[1 1 0],pclr);
                    else plot(xy(:,1),xy(:,2),'o','MarkerFaceColor','y','Color',pclr);end
                    title('City location');
                    pause(0.9)
                  
                   title('distance matrix');
                   pause(0.9)
                   
                    
                   rte=optroute([1:n 1]);
                   if dims >2,plot3(xy(rte,1),xy(rte,2),xy(rte,3),'m.-');
                   else plot(xy(rte,1),xy(rte,2),'m.-');end
                   title(sprintf('total distance = %1.4f',minDist));
                   
                   pause(0.9)
                 
                   title('Best solution history');
                   set(gca,'XLim',[1 numIter+1],'YLim',[1 1.1*max([1 disthistroy])]);
                   
                   pause(0.9)
                 
                   subplot(2,2,3);
                    pclr = ~get(0,'DefaultAxesColor');
                    if dims > 2,plot3(xy(:,1),xy(:,2),xy(:,3),'.','Color',pclr);
                    else plot(xy(:,1),xy(:,2),'.','Color',pclr);end
                    title('city location');
                    subplot(2,2,4);
                    imagesc(dmat(optroute,optroute));
                    title('distance matrix');
                    subplot(2,2,2);
                    rte = optroute([1:n 1]);
                    if dims> 2,plot3(xy(rte,1),xy(rte,2),xy(rte,3),'r.-');
                    else plot(xy(rte,1),xy(rte,2),'r.-');end
                    title(sprintf('total distance = %1.4f',minDist));
                    subplot(2,2,1);
                    plot(disthistroy,'b','LineWidth',2);
                    title('best solution histroy');
                    set(gca,'XLim',[0 numIter+1],'YLim',[0 1.1*max([1 disthistroy])]);
                end      
        %output
        if nargout 
            resultStruct = struct( ...
                'xy',       xy,...
                'dmat',      dmat, ...
                'popsize',   popsize,...
                'numIter',     numIter,...
                'optroute',    optroute,...
                'minDist',    minDist); 
                
            varargout = {resultStruct};
        end
end

function config = get_config(defaultConfig,userConfig);
    
    config = defaultConfig;
    
    defaultFields=fieldnames(defaultConfig);
    
    userFields = fieldnames(userConfig);
    nUserFields = length(userFields);
    
    for i=1:nUserFields
        userField = userFields{i};
        isField = strcmpi(defaultFields,userField);
        if nnz(isField)==1
            thisField = defaultFields{isField};
            config.(thisField)=userConfig.(userField);
        end
        
        
    end
    
end
